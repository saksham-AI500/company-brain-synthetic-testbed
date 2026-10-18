"""
sync_to_25.py
=============
Automates pushing to the user's revised target:
- Exactly 25 Pull Requests (currently 8 exist, creates 17 more)
- Exactly 25 Review Comments (currently 3 exist, creates 22 more)
- Reviews on merged PRs (>= 85%)
- Continues issues and issue comments
- Safe delay of 2.0s per write to respect GitHub anti-abuse secondary limits
- Saves checkpoints in project_context/PUSH_PROGRESS.json
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

REPO = "saksham-AI500/company-brain-synthetic-testbed"
FIXTURES = Path("data/synthetic/fixtures")
PROGRESS_FILE = Path("project_context/PUSH_PROGRESS.json")

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "issues_done": list(range(1, 98)),
        "prs_done": [37, 38],
        "commits_done": True,
        "issue_comments_count": 396,
        "review_comments_count": 3
    }

def save_progress(progress: dict):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")

def call_gh(endpoint: str, method: str = "GET", data: dict = None, retries: int = 5):
    cmd = ["gh", "api", "-X", method, endpoint, "-H", "Accept: application/vnd.github+json"]
    if data is not None:
        cmd += ["--input", "-"]

    for attempt in range(retries):
        try:
            payload = json.dumps(data).encode("utf-8") if data is not None else None
            p = subprocess.run(
                cmd,
                input=payload,
                capture_output=True,
                timeout=45
            )
            stderr = p.stderr.decode("utf-8", errors="replace")
            stdout = p.stdout.decode("utf-8", errors="replace")

            if "secondary rate limit" in stderr.lower() or "rate limit" in stderr.lower() or (p.returncode != 0 and "403" in stderr):
                wait_sec = 60 * (attempt + 1)
                print(f"  [Rate Limit / 403] Backing off {wait_sec}s (attempt {attempt+1}/{retries})...", flush=True)
                time.sleep(wait_sec)
                continue

            if p.returncode != 0:
                if "422" in stderr:
                    return {"_error": 422, "msg": stderr[:300]}
                if "404" in stderr:
                    return None
                print(f"  [API Error {p.returncode}] {stderr[:200]}, retrying in {2**attempt}s...", flush=True)
                time.sleep(2**attempt)
                continue

            if not stdout.strip():
                return {}
            return json.loads(stdout)
        except Exception as e:
            print(f"  [Exception] {e}, retrying...", flush=True)
            time.sleep(5)

    return None

def pace_write():
    time.sleep(2.0)

def sync_prs_and_reviews_to_25():
    print("\n=======================================================", flush=True)
    print("STEP: Registering PRs to reach exactly 25, and 25 Review Comments", flush=True)
    print("=======================================================", flush=True)

    progress = load_progress()

    # Get current PR count
    prs_raw = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/pulls?state=all&per_page=100", "--jq", "[.[] | {number: .number, head: .head.ref, state: .state}]"],
        text=True, errors="replace"
    )
    existing_prs = json.loads(prs_raw)
    current_pr_count = len(existing_prs)
    print(f"Current PRs on GitHub: {current_pr_count} (Target: 25)", flush=True)

    # Get current review comments count
    rev_cmts_header = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/pulls/comments?per_page=1", "-i"],
        text=True, errors="replace"
    )
    current_rev_cmts = 3
    for line in rev_cmts_header.splitlines():
        if "page=" in line and 'rel="last"' in line:
            parts = line.split("page=")
            if len(parts) > 1:
                current_rev_cmts = int(parts[-1].split(">")[0])
                break
    print(f"Current Review Comments on GitHub: {current_rev_cmts} (Target: 25)", flush=True)

    existing_refs = {p["head"] for p in existing_prs}
    target_prs = 25
    target_rev_cmts = 25

    # Register PRs from fixtures
    for n in range(1, 721):
        if current_pr_count >= target_prs:
            print(f"Reached PR target of {target_prs}!", flush=True)
            break

        branch = f"feature/pr-{n}"
        if branch in existing_refs:
            continue

        fpath = FIXTURES / "pulls" / f"{n}.json"
        if not fpath.exists():
            continue
        pr_data = json.loads(fpath.read_text(encoding="utf-8"))

        body = pr_data.get("body", "") or ""
        body += f"\n\n---\n_Synthetic fixture PR #{n} — original date: {pr_data.get('created_at')} | Author: @{pr_data.get('user', {}).get('login')}_"

        # Open PR
        pace_write()
        pr_payload = {
            "title": pr_data.get("title", f"PR #{n}"),
            "head": branch,
            "base": "main",
            "body": body,
            "draft": False
        }
        res = call_gh(f"repos/{REPO}/pulls", method="POST", data=pr_payload)
        if not res or "_error" in res:
            print(f"  [PR Error] #{n}: {res}", flush=True)
            continue

        gh_pr_num = res.get("number", n)
        current_pr_count += 1
        print(f"  [Opened PR] #{n} -> GH #{gh_pr_num}: {pr_data.get('title')[:45]} (Total PRs: {current_pr_count}/25)", flush=True)

        # Prepare review and review comments
        branch_file = f"data/synthetic/pr_branches/pr-{n:04d}/changes.txt"
        comments_to_add = []

        if current_rev_cmts < target_rev_cmts:
            fixture_comments = pr_data.get("comments", [])
            if not fixture_comments:
                fixture_comments = [{"line": 10, "body": "Verify implementation correctness and test coverage.", "user": {"login": "alex-mercer"}}]

            for cmt in fixture_comments:
                if current_rev_cmts >= target_rev_cmts:
                    break
                line_no = min(65, max(1, cmt.get("line", 10) or 10))
                c_text = f"**Review comment by @{cmt.get('user', {}).get('login')}**:\n\n{cmt.get('body')}"
                comments_to_add.append({
                    "path": branch_file,
                    "line": line_no,
                    "side": "RIGHT",
                    "body": c_text
                })
                current_rev_cmts += 1

        # Submit review
        rev_body = f"**Review by Acme Code Reviewer** — `APPROVED`\n\nAutomated synthetic dataset verification review."
        rev_payload = {
            "body": rev_body,
            "event": "COMMENT"
        }
        if comments_to_add:
            rev_payload["comments"] = comments_to_add

        pace_write()
        call_gh(f"repos/{REPO}/pulls/{gh_pr_num}/reviews", method="POST", data=rev_payload)

        # Merge or Close
        is_merged = pr_data.get("merged", True) or (pr_data.get("merged_at") is not None)
        pace_write()
        if is_merged:
            call_gh(f"repos/{REPO}/pulls/{gh_pr_num}/merge", method="PUT", data={"merge_method": "merge"})
        else:
            call_gh(f"repos/{REPO}/pulls/{gh_pr_num}", method="PATCH", data={"state": "closed"})

        progress["prs_done"] = sorted(list(set(progress.get("prs_done", []) + [gh_pr_num])))
        progress["review_comments_count"] = current_rev_cmts
        save_progress(progress)

    print(f"PRs and Review Comments complete! Total PRs: {current_pr_count}, Total Review Comments: {current_rev_cmts}", flush=True)

def verify_counts():
    print("\n=======================================================", flush=True)
    print("VERIFICATION OF CURRENT GITHUB COUNTS", flush=True)
    print("=======================================================", flush=True)

    # 1. PR count
    pr_res = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/pulls?state=all&per_page=100", "--paginate", "--jq", "length"],
        text=True, errors="replace"
    )
    pr_count = sum(int(x) for x in pr_res.strip().splitlines() if x.isdigit())

    # 2. Issues count
    iss_res = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/issues?state=all&per_page=100", "--paginate", "--jq", "[.[] | select(.pull_request|not)] | length"],
        text=True, errors="replace"
    )
    iss_count = sum(int(x) for x in iss_res.strip().splitlines() if x.isdigit())

    # 3. Commits count
    commits_header = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/commits?per_page=1", "-i"],
        text=True, errors="replace"
    )
    commit_count = 0
    for line in commits_header.splitlines():
        if "page=" in line and 'rel="last"' in line:
            parts = line.split("page=")
            if len(parts) > 1:
                commit_count = int(parts[-1].split(">")[0])
                break

    # 4. Review comments count
    rev_cmts_header = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/pulls/comments?per_page=1", "-i"],
        text=True, errors="replace"
    )
    rev_cmts_count = 0
    for line in rev_cmts_header.splitlines():
        if "page=" in line and 'rel="last"' in line:
            parts = line.split("page=")
            if len(parts) > 1:
                rev_cmts_count = int(parts[-1].split(">")[0])
                break

    # 5. Issue comments count
    iss_cmts_header = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/issues/comments?per_page=1", "-i"],
        text=True, errors="replace"
    )
    iss_cmts_count = 0
    for line in iss_cmts_header.splitlines():
        if "page=" in line and 'rel="last"' in line:
            parts = line.split("page=")
            if len(parts) > 1:
                iss_cmts_count = int(parts[-1].split(">")[0])
                break

    print(f"Pull Requests: {pr_count} (Target: 25)")
    print(f"Review Comments: {rev_cmts_count} (Target: 25)")
    print(f"Issues: {iss_count} (Target: 350)")
    print(f"Issue Comments: {iss_cmts_count} (Target: 1,434)")
    print(f"Commits: {commit_count} (Target: >= 2,000)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_counts()
    else:
        sync_prs_and_reviews_to_25()
        verify_counts()
