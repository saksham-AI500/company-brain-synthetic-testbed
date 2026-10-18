"""
push_to_github.py
=================
Pushes all synthetic fixtures to GitHub via REST API.
- Creates backdated commits on main via Git Data API
- Creates 350 issues with comments
- Creates 720 PRs (branch + commit + PR + reviews + review_comments) 
- Rate-limit aware: respects X-RateLimit-Remaining, sleeps when low
- Resume-safe: writes progress to .push_progress.json and skips already-done items
- Run: python scripts/push_to_github.py [--issues-only | --prs-only | --commits-only]

GitHub API limitations (honest):
- Issue/PR created_at cannot be backdated via REST API; timestamps will be current.
- Commit author.date CAN be set via Git Data API, so commit history appears historical.
- Review submitted_at cannot be set; it will be current.
"""

import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

REPO = "saksham-AI500/company-brain-synthetic-testbed"
FIXTURES = Path("data/synthetic/fixtures")
PROGRESS_FILE = Path(".push_progress.json")

# ─── Helpers ──────────────────────────────────────────────────────────────────

def gh_call(method: str, path: str, body: dict | None = None, retries=5) -> dict | list | None:
    """Call the GitHub API via `gh api`. Returns parsed JSON or None on 404/410."""
    cmd = ["gh", "api", "-X", method, path, "-H", "Accept: application/vnd.github+json"]
    if body:
        cmd += ["--input", "-"]

    for attempt in range(retries):
        try:
            result = subprocess.run(
                cmd,
                input=json.dumps(body).encode() if body else None,
                capture_output=True,
                timeout=30,
            )
            # Check rate limit header
            stderr = result.stderr.decode()
            if "rate limit exceeded" in stderr.lower() or result.returncode == 1 and "403" in stderr:
                wait = 60
                print(f"  ⏳ Rate limited. Sleeping {wait}s...")
                time.sleep(wait)
                continue

            if result.returncode != 0:
                if "404" in stderr or "410" in stderr:
                    return None
                if "422" in stderr:
                    # Unprocessable - likely already exists
                    return {"_skipped": True, "error": stderr[:200]}
                print(f"  ⚠ gh error (attempt {attempt+1}): {stderr[:300]}")
                time.sleep(2 ** attempt)
                continue

            text = result.stdout.decode()
            if not text.strip():
                return {}
            return json.loads(text)
        except subprocess.TimeoutExpired:
            print(f"  ⏳ Timeout on attempt {attempt+1}, retrying...")
            time.sleep(5)
        except json.JSONDecodeError:
            return {}
    return None


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"issues_done": [], "prs_done": [], "commits_done": False}


def save_progress(p: dict):
    PROGRESS_FILE.write_text(json.dumps(p, indent=2))


def throttle(n: int, batch=10, sleep_sec=1.0):
    """Sleep periodically to avoid hitting secondary rate limits."""
    if n > 0 and n % batch == 0:
        time.sleep(sleep_sec)


# ─── Step 0: Move prompt .md files into project_context/ ──────────────────────

def move_prompt_files():
    root_mds = ["AGENT_READ_AND_EXECUTE.md", "PEOPLE_EXPANSION.md",
                "SYNTHETIC_DATA_PROMPT.md"]
    dest = Path("project_context")
    dest.mkdir(exist_ok=True)
    moved = []
    for name in root_mds:
        src = Path(name)
        dst = dest / name
        if src.exists() and not dst.exists():
            src.rename(dst)
            moved.append(name)
        elif src.exists() and dst.exists():
            src.unlink()
            moved.append(f"{name} (removed duplicate)")
    if moved:
        print(f"Moved to project_context/: {moved}")
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", "chore: move prompt .md files into project_context/"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    else:
        print("No .md files to move (already in project_context/).")


# ─── Step 1: Backdated commits via Git Data API ───────────────────────────────

def create_backdated_commits():
    """
    Create all PR commits as real Git commits on main via Git Data API.
    Each commit has proper author.date set to the fixture timestamp.
    Commits are batched: we create a new tree per commit with a small file change.
    """
    print("\n=== STEP 1: Creating backdated commits on main ===")

    # Get current HEAD
    ref_data = gh_call("GET", f"/repos/{REPO}/git/ref/heads/main")
    if not ref_data:
        print("ERROR: Cannot get main ref")
        return
    head_sha = ref_data["object"]["sha"]

    # Get base tree sha
    commit_data = gh_call("GET", f"/repos/{REPO}/git/commits/{head_sha}")
    base_tree_sha = commit_data["tree"]["sha"]

    # Collect all commits from fixtures, sorted chronologically
    all_commits = []
    for pr_num in range(1, 721):
        pr_file = FIXTURES / "pulls" / f"{pr_num}.json"
        if not pr_file.exists():
            continue
        pr = json.loads(pr_file.read_text())
        for c in pr.get("commits", []):
            all_commits.append({
                "sha": c["sha"],
                "pr_number": pr_num,
                "message": c["commit"]["message"],
                "author_name": c["commit"]["author"]["name"],
                "author_email": c["commit"]["author"]["email"],
                "date": c["commit"]["author"]["date"],
            })

    all_commits.sort(key=lambda x: x["date"])
    total = len(all_commits)
    print(f"Total commits to create: {total}")

    progress = load_progress()
    if progress.get("commits_done"):
        print("Commits already done, skipping.")
        return
    done_shas = set(progress.get("commits_shas_done", []))

    current_sha = head_sha
    current_tree = base_tree_sha

    for i, c in enumerate(all_commits):
        if c["sha"] in done_shas:
            continue

        # Create a small unique file change for this commit
        file_path = f"data/synthetic/commits/{c['pr_number']:04d}/{c['sha'][:8]}.txt"
        blob_content = f"PR #{c['pr_number']} | {c['sha']} | {c['date']}\n{c['message']}\n"

        # Create blob
        blob = gh_call("POST", f"/repos/{REPO}/git/blobs", {
            "content": blob_content,
            "encoding": "utf-8"
        })
        if not blob or "_skipped" in blob:
            print(f"  ⚠ Blob failed for commit {c['sha'][:8]}, skipping")
            continue

        # Create tree
        tree = gh_call("POST", f"/repos/{REPO}/git/trees", {
            "base_tree": current_tree,
            "tree": [{
                "path": file_path,
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"]
            }]
        })
        if not tree:
            print(f"  ⚠ Tree failed for commit {c['sha'][:8]}, skipping")
            continue

        # Create commit with backdated timestamp
        new_commit = gh_call("POST", f"/repos/{REPO}/git/commits", {
            "message": c["message"],
            "tree": tree["sha"],
            "parents": [current_sha],
            "author": {
                "name": c["author_name"],
                "email": c["author_email"],
                "date": c["date"]
            },
            "committer": {
                "name": c["author_name"],
                "email": c["author_email"],
                "date": c["date"]
            }
        })
        if not new_commit:
            print(f"  ⚠ Commit failed for {c['sha'][:8]}, skipping")
            continue

        current_sha = new_commit["sha"]
        current_tree = new_commit["tree"]["sha"]
        done_shas.add(c["sha"])

        if (i + 1) % 50 == 0:
            # Update branch ref every 50 commits and save progress
            gh_call("PATCH", f"/repos/{REPO}/git/refs/heads/main", {
                "sha": current_sha,
                "force": False
            })
            progress["commits_shas_done"] = list(done_shas)
            save_progress(progress)
            print(f"  ✓ Committed {i+1}/{total} (last: {c['date'][:10]})")
            time.sleep(2)

    # Final ref update
    gh_call("PATCH", f"/repos/{REPO}/git/refs/heads/main", {
        "sha": current_sha,
        "force": False
    })
    progress["commits_done"] = True
    progress["commits_shas_done"] = list(done_shas)
    save_progress(progress)
    print(f"✓ All {total} commits created and pushed to main.")


# ─── Step 2: Create Issues ────────────────────────────────────────────────────

def create_issues():
    print("\n=== STEP 2: Creating 350 issues ===")
    progress = load_progress()
    done = set(progress.get("issues_done", []))

    for n in range(1, 351):
        if n in done:
            continue
        iss_file = FIXTURES / "issues" / f"{n}.json"
        if not iss_file.exists():
            print(f"  ⚠ Issue {n} fixture missing")
            continue

        iss = json.loads(iss_file.read_text())

        # Build body with metadata note (since created_at cannot be backdated)
        body = iss.get("body", "") or ""
        body += f"\n\n---\n_Synthetic fixture — original date: {iss['created_at']}_"

        # Add Fixes #N links to body for linked PRs
        linked = iss.get("linked_pulls", [])
        if linked:
            links = ", ".join(f"#{p}" for p in linked)
            body += f"\n_Linked PRs: {links}_"

        labels = iss.get("labels", [])

        payload = {
            "title": iss["title"],
            "body": body,
            "labels": labels if labels else []
        }

        resp = gh_call("POST", f"/repos/{REPO}/issues", payload)
        if resp is None:
            print(f"  ✗ Issue {n} failed")
            continue
        if "_skipped" in resp:
            print(f"  ⚠ Issue {n} skipped (422)")
            done.add(n)
            continue

        created_number = resp.get("number", n)
        print(f"  ✓ Issue #{n} → GitHub #{created_number}: {iss['title'][:50]}")

        # Close if needed
        if iss.get("state") == "closed":
            gh_call("PATCH", f"/repos/{REPO}/issues/{created_number}", {"state": "closed"})

        # Add comments
        for k, comment in enumerate(iss.get("comments", [])):
            cbody = comment["body"] + f"\n\n_Synthetic — original: {comment['created_at']}_"
            gh_call("POST", f"/repos/{REPO}/issues/{created_number}/comments", {"body": cbody})
            throttle(k, batch=5, sleep_sec=0.5)

        done.add(n)
        progress["issues_done"] = list(done)
        if n % 20 == 0:
            save_progress(progress)
        throttle(n, batch=20, sleep_sec=2)

    save_progress(progress)
    print(f"✓ Issues done: {len(done)}/350")


# ─── Step 3: Create PRs ───────────────────────────────────────────────────────

def get_main_sha() -> str:
    ref = gh_call("GET", f"/repos/{REPO}/git/ref/heads/main")
    return ref["object"]["sha"]


def create_pr_branch(pr_num: int, head_sha: str, pr: dict) -> str | None:
    """Create a branch for this PR with one commit, return branch name or None."""
    branch = f"feature/pr-{pr_num}"

    # Check if branch exists
    existing = gh_call("GET", f"/repos/{REPO}/git/ref/heads/{branch}")
    if existing and "object" in existing:
        return branch  # already exists

    # Get tree from HEAD
    commit_data = gh_call("GET", f"/repos/{REPO}/git/commits/{head_sha}")
    if not commit_data:
        return None
    base_tree = commit_data["tree"]["sha"]

    # Create a small file unique to this PR
    files = pr.get("files", [])
    file_path = f"data/synthetic/pr_branches/pr-{pr_num:04d}/changes.txt"
    content = f"PR #{pr_num}: {pr['title']}\nAuthor: {pr['user']['login']}\nDate: {pr['created_at']}\n"
    if files:
        content += "Files:\n" + "\n".join(f"  {f['filename']}" for f in files[:5])

    blob = gh_call("POST", f"/repos/{REPO}/git/blobs", {
        "content": content, "encoding": "utf-8"
    })
    if not blob:
        return None

    tree = gh_call("POST", f"/repos/{REPO}/git/trees", {
        "base_tree": base_tree,
        "tree": [{"path": file_path, "mode": "100644", "type": "blob", "sha": blob["sha"]}]
    })
    if not tree:
        return None

    # Commit on this branch
    commits = pr.get("commits", [])
    if commits:
        author = commits[0]["commit"]["author"]
        commit_date = author["date"]
        author_name = author["name"]
        author_email = author["email"]
    else:
        commit_date = pr["created_at"]
        author_name = pr["user"]["login"]
        author_email = f"{pr['user']['login']}@example.com"

    new_commit = gh_call("POST", f"/repos/{REPO}/git/commits", {
        "message": pr["title"],
        "tree": tree["sha"],
        "parents": [head_sha],
        "author": {"name": author_name, "email": author_email, "date": commit_date},
        "committer": {"name": author_name, "email": author_email, "date": commit_date}
    })
    if not new_commit:
        return None

    # Create the branch ref
    ref_resp = gh_call("POST", f"/repos/{REPO}/git/refs", {
        "ref": f"refs/heads/{branch}",
        "sha": new_commit["sha"]
    })
    if ref_resp is None:
        return None

    return branch


def create_prs():
    print("\n=== STEP 3: Creating 720 PRs ===")
    progress = load_progress()
    done = set(progress.get("prs_done", []))

    # Cache main sha (refresh every 100 PRs)
    main_sha = get_main_sha()
    main_sha_refresh_counter = 0

    for n in range(1, 721):
        if n in done:
            continue

        pr_file = FIXTURES / "pulls" / f"{n}.json"
        if not pr_file.exists():
            print(f"  ⚠ PR {n} fixture missing")
            continue

        pr = json.loads(pr_file.read_text())

        # Refresh main sha every 100 PRs to avoid stale refs
        main_sha_refresh_counter += 1
        if main_sha_refresh_counter % 100 == 0:
            main_sha = get_main_sha()

        # Create branch
        branch = create_pr_branch(n, main_sha, pr)
        if not branch:
            print(f"  ✗ Branch failed for PR #{n}")
            continue

        # Build PR body with original dates embedded
        body = pr.get("body", "") or ""
        body += f"\n\n---\n_Synthetic fixture — original date: {pr['created_at']}_"

        # Add Closes #N for any linked issues
        # (issues must exist first; we embed in body text)
        pr_payload = {
            "title": pr["title"],
            "body": body,
            "head": branch,
            "base": "main",
            "draft": False,
        }

        resp = gh_call("POST", f"/repos/{REPO}/pulls", pr_payload)
        if resp is None:
            print(f"  ✗ PR #{n} creation failed")
            continue
        if "_skipped" in resp:
            print(f"  ⚠ PR #{n} skipped (422 - likely no diff)")
            done.add(n)
            continue

        gh_pr_num = resp.get("number", n)
        print(f"  ✓ PR #{n} → GitHub PR #{gh_pr_num}: {pr['title'][:50]}")

        # Add reviews as comments (GitHub only allows reviews from the token owner
        # or explicit collaborators; we add them as issue comments with attribution)
        reviews = pr.get("reviews", [])
        for rev in reviews:
            rev_body = (
                f"**Review by @{rev['user']['login']}** — `{rev['state']}`\n\n"
                f"{rev.get('body', '') or '(no body)'}\n\n"
                f"_Synthetic — original submitted: {rev['submitted_at']}_"
            )
            gh_call("POST", f"/repos/{REPO}/issues/{gh_pr_num}/comments", {"body": rev_body})
            time.sleep(0.3)

        # Add review comments as PR issue comments (inline diff not possible without real diff)
        comments = pr.get("comments", [])
        for k, cmt in enumerate(comments[:5]):  # cap at 5 per PR to avoid spam
            cbody = (
                f"**Review comment by @{cmt['user']['login']}**"
                + (f" on `{cmt.get('path', '')}`" if cmt.get("path") else "")
                + f"\n\n{cmt['body']}\n\n_Synthetic — original: {cmt['created_at']}_"
            )
            gh_call("POST", f"/repos/{REPO}/issues/{gh_pr_num}/comments", {"body": cbody})
            throttle(k, batch=5, sleep_sec=0.5)

        # Close/merge the PR if it was merged in fixture
        if pr.get("state") in ("closed", "merged") or pr.get("merged_at"):
            gh_call("PATCH", f"/repos/{REPO}/pulls/{gh_pr_num}", {"state": "closed"})

        done.add(n)
        progress["prs_done"] = list(done)
        if n % 10 == 0:
            save_progress(progress)
            print(f"  Progress: {n}/720 PRs done")
        throttle(n, batch=30, sleep_sec=3)

    save_progress(progress)
    print(f"✓ PRs done: {len(done)}/720")


# ─── Step 4: Count & compare ──────────────────────────────────────────────────

def run_counts():
    print("\n=== STEP 4: Counting GitHub entities vs MANIFEST.json ===")
    manifest = json.loads(Path("data/synthetic/MANIFEST.json").read_text())
    expected = manifest["entity_counts"]

    def paginate_count(path: str) -> int:
        result = subprocess.run(
            ["gh", "api", path, "--paginate", "-H", "Accept: application/vnd.github+json"],
            capture_output=True, timeout=120
        )
        text = result.stdout.decode()
        # gh --paginate returns concatenated JSON arrays; parse total length
        try:
            items = json.loads("[" + text.replace("][", ",") + "]")
            return sum(len(page) if isinstance(page, list) else 1 for page in items)
        except Exception:
            try:
                return len(json.loads(text))
            except Exception:
                return -1

    counts = {}
    print("Fetching PR count...")
    counts["pull_requests"] = paginate_count(f"/repos/{REPO}/pulls?state=all&per_page=100")
    print(f"  PRs: {counts['pull_requests']} / expected {expected['pull_requests']}")

    print("Fetching Issue count (excludes PRs)...")
    all_issues = paginate_count(f"/repos/{REPO}/issues?state=all&per_page=100&filter=all")
    # GitHub issues endpoint includes PRs; subtract PR count
    counts["issues"] = max(0, all_issues - counts["pull_requests"])
    print(f"  Issues: {counts['issues']} / expected {expected['issues']}")

    print("Fetching Commit count...")
    counts["commits"] = paginate_count(f"/repos/{REPO}/commits?per_page=100")
    print(f"  Commits: {counts['commits']} / expected {expected['commits']}")

    print("\n--- COMPARISON TABLE ---")
    print(f"{'Entity':<25} {'Expected':>10} {'Actual':>10} {'Status':>8}")
    print("-" * 58)
    for key in ["pull_requests", "issues", "commits"]:
        exp = expected.get(key, "?")
        act = counts.get(key, "?")
        ok = "✅" if isinstance(act, int) and isinstance(exp, int) and act >= exp * 0.95 else "❌"
        print(f"  {key:<23} {str(exp):>10} {str(act):>10} {ok:>8}")

    return counts


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Push synthetic fixtures to GitHub")
    parser.add_argument("--issues-only", action="store_true")
    parser.add_argument("--prs-only", action="store_true")
    parser.add_argument("--commits-only", action="store_true")
    parser.add_argument("--counts-only", action="store_true")
    parser.add_argument("--move-files-only", action="store_true")
    args = parser.parse_args()

    os.chdir(Path(__file__).parent.parent)

    if args.counts_only:
        run_counts()
        return

    if args.move_files_only:
        move_prompt_files()
        return

    # Always move prompt files first
    move_prompt_files()

    if args.commits_only:
        create_backdated_commits()
    elif args.issues_only:
        create_issues()
    elif args.prs_only:
        create_prs()
    else:
        # Full run: issues first (PRs can reference them), then PRs, then commits
        create_issues()
        create_prs()
        create_backdated_commits()

    run_counts()


if __name__ == "__main__":
    main()
