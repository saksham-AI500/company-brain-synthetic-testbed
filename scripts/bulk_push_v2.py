#!/usr/bin/env python3
"""
bulk_push_v2.py - Comprehensive script to push all remaining synthetic data to GitHub.
Resumes from where it left off using .push_progress_v2.json.
"""

import json
import os
import subprocess
import sys
import time
import random
from pathlib import Path

REPO = "saksham-AI500/company-brain-synthetic-testbed"
FIXTURES = Path("data/synthetic/fixtures")
PROGRESS_FILE = Path(".push_progress_v2.json")
RATE_LIMIT_DELAY = 0.8
MAX_RETRIES = 5

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {
        "issues_done": [],
        "prs_done": [],
        "pr_reviews_done": [],
        "pr_review_comments_done": {},
        "issue_comments_done": {},
        "pr_mapping": {},
    }

def save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")

def gh_api(method, endpoint, data=None, retries=0):
    cmd = ["gh", "api", "--method", method, endpoint]
    if data:
        for k, v in data.items():
            if isinstance(v, bool):
                cmd += ["-f", f"{k}={'true' if v else 'false'}"]
            elif isinstance(v, int):
                cmd += ["-F", f"{k}={v}"]
            elif isinstance(v, list):
                for item in v:
                    cmd += ["-f", f"{k}[]={item}"]
            else:
                cmd += ["-f", f"{k}={v}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout) if result.stdout.strip() else {}
        if "secondary rate limit" in result.stderr.lower() or ("403" in result.stderr and "rate" in result.stderr.lower()):
            wait = 60 * (retries + 1)
            print(f"  Rate limit, waiting {wait}s...")
            time.sleep(wait)
            if retries < MAX_RETRIES:
                return gh_api(method, endpoint, data, retries + 1)
        if "422" in result.stderr:
            return None
        if retries < MAX_RETRIES:
            time.sleep(5 * (retries + 1))
            return gh_api(method, endpoint, data, retries + 1)
        print(f"  FAILED: {result.stderr[:150]}")
        return None
    except subprocess.TimeoutExpired:
        if retries < MAX_RETRIES:
            time.sleep(10)
            return gh_api(method, endpoint, data, retries + 1)
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def get_existing_on_github():
    print("Fetching current GitHub state...")
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/pulls?state=all&per_page=100", "--paginate", "--jq", "[.[].number]"],
        capture_output=True, text=True
    )
    pr_numbers = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            try: pr_numbers.extend(json.loads(line))
            except: pass
    result2 = subprocess.run(
        ["gh", "api", f"repos/{REPO}/issues?state=all&per_page=100", "--paginate", "--jq", "[.[] | select(.pull_request == null) | .number]"],
        capture_output=True, text=True
    )
    issue_numbers = []
    for line in result2.stdout.strip().split("\n"):
        if line.strip():
            try: issue_numbers.extend(json.loads(line))
            except: pass
    print(f"  PRs on GitHub: {len(pr_numbers)}")
    print(f"  Issues on GitHub: {len(issue_numbers)}")
    return set(pr_numbers), set(issue_numbers)

def get_available_labels():
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/labels?per_page=100", "--jq", "[.[].name]"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return set(json.loads(result.stdout))
    return set()

def ensure_label(label, available_labels):
    if label in available_labels:
        return
    colors = {
        "bug": "d73a4a", "enhancement": "a2eeef", "documentation": "0075ca",
        "question": "d876e3", "help wanted": "008672", "good first issue": "7057ff",
        "invalid": "e4e669", "wontfix": "ffffff", "duplicate": "cfd3d7",
        "feature": "84b6eb", "performance": "0052cc", "security": "e11d48",
        "refactor": "fbca04", "test": "bfd4f2", "ci": "f9d0c4",
    }
    color = colors.get(label, "ededed")
    gh_api("POST", f"repos/{REPO}/labels", {"name": label, "color": color})
    available_labels.add(label)
    time.sleep(0.3)

def create_issue(fixture, available_labels):
    labels = fixture.get("labels", [])
    for lbl in labels:
        ensure_label(lbl, available_labels)
    data = {"title": fixture["title"], "body": fixture.get("body", "") or f"Issue #{fixture['number']}"}
    result = gh_api("POST", f"repos/{REPO}/issues", data)
    if not result:
        return None
    num = result.get("number")
    if labels and num:
        time.sleep(RATE_LIMIT_DELAY)
        gh_api("POST", f"repos/{REPO}/issues/{num}/labels", {"labels": labels})
    if fixture.get("state") == "closed" and num:
        time.sleep(RATE_LIMIT_DELAY)
        gh_api("PATCH", f"repos/{REPO}/issues/{num}", {"state": "closed"})
    return num

def add_issue_comments(issue_number, comments, progress):
    key = str(issue_number)
    done_count = progress.get("issue_comments_done", {}).get(key, 0)
    for i, comment in enumerate(comments[done_count:], done_count):
        time.sleep(RATE_LIMIT_DELAY)
        result = gh_api("POST", f"repos/{REPO}/issues/{issue_number}/comments", {
            "body": comment.get("body", "Comment.") or "Comment."
        })
        if result:
            if "issue_comments_done" not in progress:
                progress["issue_comments_done"] = {}
            progress["issue_comments_done"][key] = i + 1

def get_head_sha():
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/refs/heads/main", "--jq", ".object.sha"],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None

def create_branch(branch_name, head_sha):
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/refs/heads/{branch_name}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return True
    result2 = gh_api("POST", f"repos/{REPO}/git/refs", {
        "ref": f"refs/heads/{branch_name}",
        "sha": head_sha
    })
    return result2 is not None

def commit_to_branch(branch_name, pr_number, fixture, head_sha):
    # Get branch SHA
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/refs/heads/{branch_name}", "--jq", ".object.sha"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    branch_sha = result.stdout.strip()
    
    # Get tree SHA
    result2 = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/commits/{branch_sha}", "--jq", ".tree.sha"],
        capture_output=True, text=True
    )
    if result2.returncode != 0:
        return None
    tree_sha = result2.stdout.strip()
    
    # Create blob
    blob_content = f"# PR {pr_number}\n\n{fixture.get('title','')}\n\n{fixture.get('body','')[:200]}\n"
    blob_result = gh_api("POST", f"repos/{REPO}/git/blobs", {"content": blob_content, "encoding": "utf-8"})
    if not blob_result:
        return None
    blob_sha = blob_result.get("sha")
    
    # Create tree
    filename = f".pr_meta/pr_{pr_number}.md"
    cmd = ["gh", "api", "--method", "POST", f"repos/{REPO}/git/trees",
           "-f", f"base_tree={tree_sha}",
           "-f", f"tree[][path]={filename}",
           "-f", "tree[][mode]=100644",
           "-f", "tree[][type]=blob",
           "-f", f"tree[][sha]={blob_sha}"]
    result3 = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result3.returncode != 0:
        return None
    new_tree_sha = json.loads(result3.stdout).get("sha")
    
    # Create commit
    author = fixture.get("user", {}).get("login", "dev-bot")
    created_at = fixture.get("created_at", "2025-10-01T09:00:00Z")
    msg = fixture.get("title", f"PR {pr_number} changes")
    
    cmd4 = ["gh", "api", "--method", "POST", f"repos/{REPO}/git/commits",
            "-f", f"message={msg}",
            "-f", f"tree={new_tree_sha}",
            "-f", f"parents[]={branch_sha}",
            "-f", f"author[name]={author}",
            "-f", f"author[email]={author}@example.com",
            "-f", f"author[date]={created_at}",
            "-f", f"committer[name]={author}",
            "-f", f"committer[email]={author}@example.com",
            "-f", f"committer[date]={created_at}"]
    result4 = subprocess.run(cmd4, capture_output=True, text=True, timeout=30)
    if result4.returncode != 0:
        return None
    commit_sha = json.loads(result4.stdout).get("sha")
    
    # Update ref
    gh_api("PATCH", f"repos/{REPO}/git/refs/heads/{branch_name}", {"sha": commit_sha, "force": "true"})
    return commit_sha

def create_pr(fixture, head_sha):
    pr_num = fixture["number"]
    branch_name = f"feature/pr-{pr_num}"
    
    time.sleep(RATE_LIMIT_DELAY)
    if not create_branch(branch_name, head_sha):
        print(f"    Failed to create branch for PR {pr_num}")
        return None
    
    time.sleep(RATE_LIMIT_DELAY)
    commit_to_branch(branch_name, pr_num, fixture, head_sha)
    
    time.sleep(RATE_LIMIT_DELAY)
    body = fixture.get("body") or f"PR #{pr_num}: {fixture.get('title', '')}"
    result = gh_api("POST", f"repos/{REPO}/pulls", {
        "title": fixture["title"],
        "body": body,
        "head": branch_name,
        "base": "main"
    })
    if not result:
        return None
    actual_num = result.get("number")
    return actual_num

def add_review_comments(pr_number, fixture, progress):
    comments = fixture.get("comments", [])
    if not comments:
        return
    done_count = progress.get("pr_review_comments_done", {}).get(str(pr_number), 0)
    if done_count >= len(comments):
        return
    
    # Get PR head SHA
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/pulls/{pr_number}", "--jq", ".head.sha"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return
    head_sha = result.stdout.strip()
    
    for i, comment in enumerate(comments[done_count:], done_count):
        time.sleep(RATE_LIMIT_DELAY)
        path = comment.get("path", "README.md")
        line = comment.get("line", 1)
        body = comment.get("body", "Review comment.") or "Review comment."
        
        cmd = ["gh", "api", "--method", "POST", f"repos/{REPO}/pulls/{pr_number}/comments",
               "-f", f"body={body}",
               "-f", f"commit_id={head_sha}",
               "-f", f"path={path}",
               "-F", f"line={line}",
               "-f", "side=RIGHT"]
        result2 = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result2.returncode == 0:
            if "pr_review_comments_done" not in progress:
                progress["pr_review_comments_done"] = {}
            progress["pr_review_comments_done"][str(pr_number)] = i + 1
        else:
            # Fallback to issue comment
            gh_api("POST", f"repos/{REPO}/issues/{pr_number}/comments", {"body": body})
            if "pr_review_comments_done" not in progress:
                progress["pr_review_comments_done"] = {}
            progress["pr_review_comments_done"][str(pr_number)] = i + 1

def add_pr_review(pr_number, fixture, progress):
    reviews = fixture.get("reviews", [])
    if not reviews:
        return
    if str(pr_number) in progress.get("pr_reviews_done", []):
        return
    
    for review in reviews[:1]:  # One review per PR
        time.sleep(RATE_LIMIT_DELAY)
        state = review.get("state", "COMMENT")
        if state not in ["APPROVED", "REQUEST_CHANGES", "COMMENT"]:
            state = "COMMENT"
        body = review.get("body", "Reviewed.") or "Reviewed."
        result = gh_api("POST", f"repos/{REPO}/pulls/{pr_number}/reviews", {
            "body": body,
            "event": state
        })
        if result:
            if "pr_reviews_done" not in progress:
                progress["pr_reviews_done"] = []
            progress["pr_reviews_done"].append(str(pr_number))
            break

def close_pr(pr_number, fixture):
    state = fixture.get("state", "open")
    if state == "open":
        return
    merged_at = fixture.get("merged_at")
    time.sleep(RATE_LIMIT_DELAY)
    if merged_at:
        result = gh_api("PUT", f"repos/{REPO}/pulls/{pr_number}/merge", {
            "merge_method": "merge",
            "commit_title": f"Merge PR #{pr_number}"
        })
        if result and result.get("merged"):
            return
    gh_api("PATCH", f"repos/{REPO}/issues/{pr_number}", {"state": "closed"})

def main():
    print("=" * 60)
    print("Bulk Push v2")
    print("=" * 60)
    
    progress = load_progress()
    existing_prs, existing_issues = get_existing_on_github()
    available_labels = get_available_labels()
    
    issue_files = sorted(FIXTURES.glob("issues/*.json"), key=lambda x: int(x.stem))
    pr_files = sorted(FIXTURES.glob("pulls/*.json"), key=lambda x: int(x.stem))
    
    issues_done = set(progress.get("issues_done", []))
    prs_done = set(progress.get("prs_done", []))
    
    missing_issues = [f for f in issue_files if int(f.stem) not in issues_done and int(f.stem) not in existing_issues]
    missing_prs = [f for f in pr_files if int(f.stem) not in prs_done]
    
    print(f"\nMissing issues: {len(missing_issues)}")
    print(f"Missing PRs: {len(missing_prs)}")
    
    # STEP 1: Issues
    print(f"\n[STEP 1] Creating {len(missing_issues)} issues...")
    for i, f in enumerate(missing_issues):
        fixture = json.loads(f.read_text(encoding="utf-8"))
        fn = fixture["number"]
        print(f"  [{i+1}/{len(missing_issues)}] Issue #{fn}: {fixture['title'][:50]}")
        time.sleep(RATE_LIMIT_DELAY)
        actual = create_issue(fixture, available_labels)
        if actual:
            issues_done.add(fn)
            progress["issues_done"] = list(issues_done)
            if fixture.get("comments"):
                add_issue_comments(actual, fixture["comments"], progress)
            if i % 20 == 19:
                save_progress(progress)
                print(f"  Saved progress ({i+1} done)")
    save_progress(progress)
    
    # STEP 2: PRs
    print(f"\n[STEP 2] Creating {len(missing_prs)} PRs...")
    head_sha = get_head_sha()
    if not head_sha:
        print("ERROR: Could not get HEAD SHA")
        sys.exit(1)
    
    pr_mapping = progress.get("pr_mapping", {})
    
    for i, f in enumerate(missing_prs):
        fixture = json.loads(f.read_text(encoding="utf-8"))
        fn = fixture["number"]
        print(f"  [{i+1}/{len(missing_prs)}] PR #{fn}: {fixture['title'][:50]}")
        
        actual = create_pr(fixture, head_sha)
        if actual:
            prs_done.add(fn)
            pr_mapping[str(fn)] = actual
            progress["prs_done"] = list(prs_done)
            progress["pr_mapping"] = pr_mapping
            
            if fixture.get("comments"):
                add_review_comments(actual, fixture, progress)
            if fixture.get("reviews"):
                add_pr_review(actual, fixture, progress)
            if fixture.get("state") != "open":
                close_pr(actual, fixture)
            
            if i % 10 == 9:
                save_progress(progress)
                print(f"  Saved progress ({i+1} done)")
    
    save_progress(progress)
    
    # Final report
    print("\n" + "=" * 60)
    final_prs, final_issues = get_existing_on_github()
    print(f"DONE: PRs={len(final_prs)}/720  Issues={len(final_issues)}/350")

if __name__ == "__main__":
    main()
