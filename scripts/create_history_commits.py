import json
import subprocess
from datetime import datetime
from pathlib import Path

fixtures = Path('data/synthetic/fixtures')
commits = []
for p in (fixtures / 'pulls').glob('*.json'):
    data = json.loads(p.read_text(encoding='utf-8'))
    pr_num = data['number']
    for c in data.get('commits', []):
        author = c['commit']['author']
        commits.append({
            'pr_number': pr_num,
            'sha': c['sha'],
            'author_name': author['name'],
            'author_email': author['email'],
            'date': author['date'],
            'message': c['commit']['message'],
        })

commits.sort(key=lambda x: x['date'])
print(f'Total commits to fast-import: {len(commits)}')

head_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print('Current HEAD sha:', head_sha)

stream = []
for idx, c in enumerate(commits, start=1):
    ts = int(datetime.fromisoformat(c['date'].replace('Z', '+00:00')).timestamp())
    msg = c['message']
    name = c['author_name']
    email = c['author_email']
    stream.append('commit refs/heads/main')
    stream.append(f'mark :{idx}')
    stream.append(f'author {name} <{email}> {ts} +0000')
    stream.append(f'committer {name} <{email}> {ts} +0000')
    msg_bytes = msg.encode('utf-8')
    stream.append(f'data {len(msg_bytes)}')
    stream.append(msg)
    if idx == 1:
        stream.append(f'from {head_sha}')
    file_path = f"data/synthetic/commits/{c['pr_number']:04d}/{c['sha'][:8]}.txt"
    content = f"PR #{c['pr_number']} | {c['sha']} | {c['date']}\n{c['message']}\n"
    content_bytes = content.encode('utf-8')
    stream.append(f'M 100644 inline {file_path}')
    stream.append(f'data {len(content_bytes)}')
    stream.append(content)
    stream.append('')

payload = '\n'.join(stream) + '\n'
print('Fast-import payload generated, lines:', len(stream))

p = subprocess.run(['git', 'fast-import'], input=payload.encode('utf-8'), capture_output=True)
print('fast-import returncode:', p.returncode)
if p.returncode != 0:
    print('Stderr:', p.stderr.decode()[:500])
else:
    print('Fast-import successful!')

new_head = subprocess.check_output(['git', 'rev-parse', 'refs/heads/main'], text=True).strip()
print('New main sha:', new_head)

subprocess.run(['git', 'reset', '--hard', 'main'])
count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], text=True).strip()
print('Total commits on branch main:', count)
