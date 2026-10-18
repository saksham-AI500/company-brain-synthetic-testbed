"""
complete_sync_dataset.py
========================
Updated to match the user's revised expedited targets:
- Issues: exactly 210
- Comments: >= 600
- Pull Requests: 25
- Review Comments: 25
- Commits: >= 2,000
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

REPO = "saksham-AI500/company-brain-synthetic-testbed"
FIXTURES_DIR = Path("data/synthetic/fixtures")
PROGRESS_FILE = Path("project_context/PUSH_PROGRESS.json")

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "issues_done": [],
        "prs_done": list(range(1, 26)),
        "commits_done": True,
        "issue_comments_count": 0,
        "review_comments_count": 25
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
                wait_sec = min(180, 45 * (attempt + 1))
                print(f"  [Rate Limit / 403] Backing off {wait_sec}s (attempt {attempt+1}/{retries})...", flush=True)
                time.sleep(wait_sec)
                continue

            if p.returncode != 0:
                if "422" in stderr:
                    return {"_error": 422, "msg": stderr[:300]}
                if "404" in stderr:
                    return None
                print(f"  [Error {p.returncode}] {stderr[:200]}, retrying in {2**attempt}s...", flush=True)
                time.sleep(2**attempt)
                continue

            if not stdout.strip():
                return {}
            return json.loads(stdout)
        except Exception as e:
            print(f"  [Exception] {e}, retrying...", flush=True)
            time.sleep(4)

    return None

def pace_write():
    time.sleep(0.65)

def get_current_counts():
    iss_out = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/issues?state=all&per_page=100", "--paginate", "--jq", "[.[] | select(.pull_request|not) | .number]"],
        text=True, errors="replace"
    )
    issues = []
    for line in iss_out.strip().splitlines():
        if line.strip():
            try:
                issues.extend(json.loads(line))
            except Exception:
                pass

    cmt_header = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/issues/comments?per_page=1", "-i"],
        text=True, errors="replace"
    )
    comments_count = 0
    for line in cmt_header.splitlines():
        if "page=" in line and 'rel="last"' in line:
            parts = line.split("page=")
            if len(parts) > 1:
                comments_count = int(parts[-1].split(">")[0])
                break

    return len(issues), set(issues), comments_count

def run_sync():
    print("=======================================================", flush=True)
    print("Starting Fast Issue Sync (Target: 210 Issues, >= 600 Comments)", flush=True)
    print("=======================================================", flush=True)

    progress = load_progress()
    issue_count, existing_issues, comments_count = get_current_counts()
    print(f"Current Issues on GitHub: {issue_count} (Target: 210)", flush=True)
    print(f"Current Issue Comments on GitHub: {comments_count} (Target: >= 600)", flush=True)

    TARGET_ISSUES = 210
    TARGET_COMMENTS = 600

    fixtures = {}
    for p in (FIXTURES_DIR / "issues").glob("*.json"):
        fixtures[int(p.stem)] = json.loads(p.read_text(encoding="utf-8"))

    processed_fixtures = set(progress.get("issues_done", []))

    for fn in range(1, 351):
        if issue_count >= TARGET_ISSUES:
            print(f"\nTarget of {TARGET_ISSUES} issues reached!", flush=True)
            break

        if fn in processed_fixtures:
            continue

        fdata = fixtures.get(fn)
        if not fdata:
            continue

        body = fdata.get("body", "") or ""
        body += f"\n\n---\n_Synthetic fixture #{fn} — original date: {fdata.get('created_at')} | Author: @{fdata.get('user', {}).get('login')}_"
        linked = fdata.get("linked_pulls", [])
        if linked:
            body += f"\n_Linked PRs: {', '.join(f'#{p}' for p in linked)}_"

        payload = {
            "title": fdata.get("title", f"Issue #{fn}"),
            "body": body,
            "labels": fdata.get("labels", [])
        }

        pace_write()
        res = call_gh(f"repos/{REPO}/issues", method="POST", data=payload)
        if not res or "_error" in res:
            print(f"  [Failed to create] #{fn}: {res}", flush=True)
            continue

        gh_issue_num = res.get("number")
        issue_count += 1
        existing_issues.add(gh_issue_num)
        print(f"  [Issue {issue_count}/{TARGET_ISSUES}] Fixture #{fn} -> GH #{gh_issue_num}: {fdata.get('title')[:45]}", flush=True)

        if fdata.get("state") == "closed":
            pace_write()
            call_gh(f"repos/{REPO}/issues/{gh_issue_num}", method="PATCH", data={"state": "closed"})

        # Only add comments if comments_count is below TARGET_COMMENTS
        if comments_count < TARGET_COMMENTS:
            for cmt in fdata.get("comments", []):
                if comments_count >= TARGET_COMMENTS:
                    break
                cbody = cmt.get("body", "") + f"\n\n_Synthetic fixture — @{cmt.get('user', {}).get('login')} at {cmt.get('created_at')}_"
                pace_write()
                call_gh(f"repos/{REPO}/issues/{gh_issue_num}/comments", method="POST", data={"body": cbody})
                comments_count += 1

        processed_fixtures.add(fn)
        progress["issues_done"] = sorted(list(processed_fixtures))
        progress["issue_comments_count"] = comments_count
        save_progress(progress)

    print("\n=======================================================", flush=True)
    print(f"SYNC COMPLETED! Issues: {issue_count}/210, Comments: {comments_count}", flush=True)
    print("=======================================================", flush=True)

if __name__ == "__main__":
    run_sync()
