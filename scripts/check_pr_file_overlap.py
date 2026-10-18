import json
from pathlib import Path
from collections import defaultdict

fixtures = Path('data/synthetic/fixtures')
file_prs = defaultdict(list)
for n in range(1, 721):
    f = fixtures / 'pulls' / f'{n}.json'
    if not f.exists():
        continue
    pr = json.loads(f.read_text(encoding='utf-8'))
    for file_obj in pr.get('files', []):
        file_prs[file_obj['filename']].append(n)

overlapping = {k: v for k, v in file_prs.items() if len(v) > 1}
print(f"Total unique files touched across all PRs: {len(file_prs)}")
print(f"Files touched by >1 PR: {len(overlapping)}")
