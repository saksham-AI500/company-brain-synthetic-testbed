import json
import subprocess
from datetime import datetime
from pathlib import Path

fixtures = Path('data/synthetic/fixtures')
head_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print('Current HEAD sha:', head_sha)

stream = []
for n in range(1, 721):
    f = fixtures / 'pulls' / f'{n}.json'
    if not f.exists():
        continue
    pr = json.loads(f.read_text(encoding='utf-8'))
    branch_ref = f"refs/heads/feature/pr-{n}"
    commits = pr.get('commits', [])
    if commits:
        author = commits[0]['commit']['author']
        author_name = author['name']
        author_email = author['email']
        date_str = author['date']
    else:
        author_name = pr['user']['login']
        author_email = f"{pr['user']['login']}@example.com"
        date_str = pr['created_at']
    ts = int(datetime.fromisoformat(date_str.replace('Z', '+00:00')).timestamp())

    stream.append(f'commit {branch_ref}')
    stream.append(f'mark :{n}')
    stream.append(f'author {author_name} <{author_email}> {ts} +0000')
    stream.append(f'committer {author_name} <{author_email}> {ts} +0000')
    msg = pr['title']
    msg_bytes = msg.encode('utf-8')
    stream.append(f'data {len(msg_bytes)}')
    stream.append(msg)
    stream.append(f'from {head_sha}')

    file_path = f"data/synthetic/pr_branches/pr-{n:04d}/changes.txt"
    # Provide 70 lines so any comment up to line 65 is well within diff
    lines = [f"PR #{n}: {pr['title']}", f"Author: {author_name} <{author_email}>", f"Date: {date_str}"]
    for line_idx in range(4, 75):
        lines.append(f"// line {line_idx} implementation code for module")
    content = '\n'.join(lines) + '\n'
    content_bytes = content.encode('utf-8')

    stream.append(f'M 100644 inline {file_path}')
    stream.append(f'data {len(content_bytes)}')
    stream.append(content)
    stream.append('')

payload = '\n'.join(stream) + '\n'
print(f"Fast-import stream lines: {len(stream)}")

p = subprocess.run(['git', 'fast-import'], input=payload.encode('utf-8'), capture_output=True)
print(f"fast-import returncode: {p.returncode}")
if p.returncode != 0:
    print('Stderr:', p.stderr.decode()[:500])
else:
    print('All 720 PR branches created locally in git!')
