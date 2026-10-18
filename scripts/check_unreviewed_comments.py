import json
from pathlib import Path

fixtures = Path('data/synthetic/fixtures')
cmts_without_revs = 0
for n in range(1, 721):
    f = fixtures / 'pulls' / f'{n}.json'
    if not f.exists():
        continue
    pr = json.loads(f.read_text(encoding='utf-8'))
    revs = pr.get('reviews', [])
    cmts = pr.get('comments', [])
    if cmts and not revs:
        cmts_without_revs += len(cmts)

print(f"Comments on PRs with no reviews: {cmts_without_revs}")
