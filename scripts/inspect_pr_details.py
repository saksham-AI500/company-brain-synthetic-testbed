import json
from pathlib import Path

fixtures = Path('data/synthetic/fixtures')
total_revs = 0
total_rev_cmts = 0
prs_with_revs = 0
merged_count = 0
merged_with_revs = 0

for n in range(1, 721):
    f = fixtures / 'pulls' / f'{n}.json'
    if not f.exists():
        continue
    pr = json.loads(f.read_text(encoding='utf-8'))
    revs = pr.get('reviews', [])
    cmts = pr.get('comments', [])
    total_revs += len(revs)
    total_rev_cmts += len(cmts)
    if revs:
        prs_with_revs += 1
    is_merged = pr.get('merged', False) or (pr.get('merged_at') is not None)
    if is_merged:
        merged_count += 1
        if revs:
            merged_with_revs += 1

print(f"Total PRs: 720")
print(f"Total reviews: {total_revs}")
print(f"Total review comments: {total_rev_cmts}")
print(f"Merged PRs: {merged_count}")
print(f"Merged PRs with reviews: {merged_with_revs} ({merged_with_revs/merged_count*100:.2f}%)")
