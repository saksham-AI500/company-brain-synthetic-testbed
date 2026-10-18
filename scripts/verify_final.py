import subprocess
import json
import re

REPO = "saksham-AI500/company-brain-synthetic-testbed"

def parse_last_page(header_text: str) -> int:
    match = re.search(r'page=(\d+)[^>]*>;\s*rel="last"', header_text)
    if match:
        return int(match.group(1))
    return 0

# 1. PR count
pr_out = subprocess.check_output(['gh', 'api', f'repos/{REPO}/pulls?state=all&per_page=100', '--paginate', '--jq', 'length'], text=True)
pr_count = sum(int(x) for x in pr_out.strip().splitlines() if x.isdigit())

# 2. Issues count (excluding PRs)
iss_out = subprocess.check_output(['gh', 'api', f'repos/{REPO}/issues?state=all&per_page=100', '--paginate', '--jq', '[.[] | select(.pull_request|not)] | length'], text=True)
iss_count = sum(int(x) for x in iss_out.strip().splitlines() if x.isdigit())

# 3. Commits count
cmt_head = subprocess.check_output(['gh', 'api', f'repos/{REPO}/commits?per_page=1', '-i'], text=True)
commit_count = parse_last_page(cmt_head)

# 4. Review comments count
rcmt_head = subprocess.check_output(['gh', 'api', f'repos/{REPO}/pulls/comments?per_page=1', '-i'], text=True)
rcmt_count = parse_last_page(rcmt_head)

# 5. Issue comments count
icmt_head = subprocess.check_output(['gh', 'api', f'repos/{REPO}/issues/comments?per_page=1', '-i'], text=True)
icmt_count = parse_last_page(icmt_head)

# 6. Reviews on merged PRs
prs = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/pulls?state=all&per_page=100'], text=True))
merged_prs = [p for p in prs if p.get('merged_at')]
reviewed_count = 0
for p in merged_prs:
    revs = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/pulls/{p["number"]}/reviews'], text=True))
    if len(revs) > 0:
        reviewed_count += 1
pct_reviewed = (reviewed_count / len(merged_prs) * 100) if merged_prs else 0

print("=" * 60)
print("FINAL GITHUB API VERIFICATION")
print("=" * 60)
print(f"PULL_REQUESTS: {pr_count}")
print(f"ISSUES: {iss_count}")
print(f"COMMITS: {commit_count}")
print(f"REVIEW_COMMENTS: {rcmt_count}")
print(f"ISSUE_COMMENTS: {icmt_count}")
print(f"MERGED_PRS_TOTAL: {len(merged_prs)}")
print(f"MERGED_PRS_REVIEWED: {reviewed_count} ({pct_reviewed:.1f}%)")
