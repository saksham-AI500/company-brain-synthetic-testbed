import json
from pathlib import Path

fixtures = Path('data/synthetic/fixtures')
max_line = 0
all_paths = set()
for n in range(1, 721):
    f = fixtures / 'pulls' / f'{n}.json'
    if not f.exists():
        continue
    pr = json.loads(f.read_text(encoding='utf-8'))
    for c in pr.get('comments', []):
        line = c.get('line', 1) or 1
        if line > max_line:
            max_line = line
        all_paths.add(c.get('path', ''))

print(f"Max line across all comments: {max_line}")
print(f"Total unique paths: {len(all_paths)}")
