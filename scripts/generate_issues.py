"""
Deterministic Issues and Comments Generator for Acme Platform Inc.
Generates 350 issues with 1,200+ issue comments and 40% PR linking.
"""
import os
import json
import yaml
import random
from datetime import datetime, timedelta

SEED = 20260930

def load_plan():
    with open("data/synthetic/PLAN.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run():
    print("Generating 350 Issues and 1,200+ issue comments deterministically...")
    rng = random.Random(SEED + 100)
    plan = load_plan()
    roster = plan["roster"]
    modules = plan["modules"]

    people_by_login = {p["login"]: p for p in roster}
    humans = [p for p in roster if p["group"] in ("current", "former", "contractor")]

    start_date = datetime(2025, 10, 1, 9, 0, 0)
    end_date = datetime(2026, 9, 30, 18, 0, 0)
    total_seconds = int((end_date - start_date).total_seconds())

    issues_dir = os.path.join("data", "synthetic", "fixtures", "issues")
    os.makedirs(issues_dir, exist_ok=True)
    pulls_dir = os.path.join("data", "synthetic", "fixtures", "pulls")

    total_issues = 350
    linked_issue_count = 140 # Exactly 40%

    # Map of linked issue -> PR number
    # Planted links:
    # Issue #42 -> [PR 108 (false link), PR 145 (real fix)]
    # Issue #78 -> PR 220 (auth token migration tracking)
    linked_pairs = {42: [108, 145], 78: [220]}

    # Select 138 other PRs to link to the remaining 138 linked issues
    available_prs = [i for i in range(1, 650) if i not in (108, 145, 220, 488)]
    rng.shuffle(available_prs)

    linked_issues = set(range(1, linked_issue_count + 1))
    pr_idx = 0
    for iss_num in sorted(linked_issues):
        if iss_num not in linked_pairs:
            linked_pairs[iss_num] = [available_prs[pr_idx]]
            pr_idx += 1

    total_issue_comments = 0
    issues = []
    events = []

    # Read existing events if available
    events_path = os.path.join("data", "synthetic", "fixtures", "events.jsonl")
    if os.path.exists(events_path):
        with open(events_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))

    # Pre-determine timestamps for issues
    time_step = total_seconds / total_issues

    for iss_num in range(1, total_issues + 1):
        sec_offset = int((iss_num - 1) * time_step + rng.randint(-1800, 1800))
        sec_offset = max(0, min(total_seconds - 3600, sec_offset))
        iss_created = start_date + timedelta(seconds=sec_offset)
        iso_created = iss_created.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Planted issues
        if iss_num == 42:
            # Q1, Q4
            title = "Checkout timeout under heavy concurrency"
            body = "Customers experience intermittent 504 gateway timeouts during checkout bursts. See discussion in PR #108.\nInvestigating database connection pool deadlock."
            state = "closed"
            mod = "payments/"
            labels = ["bug", "payments", "sev-2"]
            author_login = "priya-sharma"
            closed_at = (iss_created + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif iss_num == 78:
            # Q2
            title = "Auth token v2 migration tracker"
            body = "Tracking issue for migration to asymmetric JWT signing and token v2 architecture.\nSpecification documented in docs/guides/auth-token-migration.md."
            state = "open"
            mod = "auth/"
            labels = ["feature", "auth", "migration"]
            author_login = "ananya-rao"
            closed_at = None
        else:
            mod = rng.choice(modules)
            mod_clean = mod.strip("/").replace("/", "-")
            itype = rng.choice(["bug", "feature", "task", "incident", "perf"])
            title = f"{itype.upper()}: {mod_clean} improvements for {rng.choice(['latency', 'throughput', 'reliability', 'security', 'caching'])}"
            body = f"Detailed description for {itype} tracking in module {mod}."
            labels = [itype, mod_clean]

            # Eligible author
            cur_d_str = iss_created.strftime("%Y-%m-%d")
            cands = [p for p in humans if p["start_date"] <= cur_d_str and (p["end_date"] is None or p["end_date"] >= cur_d_str)]
            author_login = rng.choice(cands)["login"]

            # State: 70% closed, 30% open
            is_closed = (rng.random() < 0.70)
            state = "closed" if is_closed else "open"
            closed_at = (iss_created + timedelta(days=rng.randint(2, 30))).strftime("%Y-%m-%dT%H:%M:%SZ") if is_closed else None

        # Determine linked pulls
        pull_links = linked_pairs.get(iss_num, [])

        # Generate 2 to 6 issue comments per issue
        comments = []
        num_comments = rng.randint(2, 6)
        com_cur = iss_created
        for c_idx in range(num_comments):
            com_cur = com_cur + timedelta(hours=rng.randint(2, 24))
            total_issue_comments += 1
            com_d_str = com_cur.strftime("%Y-%m-%d")
            c_cands = [p for p in humans if p["start_date"] <= com_d_str and (p["end_date"] is None or p["end_date"] >= com_d_str)]
            com_author = rng.choice(c_cands)["login"]
            c_obj = {
                "id": 70000 + total_issue_comments,
                "user": {"login": com_author, "type": "User"},
                "body": f"Comment #{total_issue_comments} on issue #{iss_num}: updates from triage and reproduction steps.",
                "created_at": com_cur.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            comments.append(c_obj)

        issue_obj = {
            "id": 2000000 + iss_num,
            "number": iss_num,
            "title": title,
            "body": body,
            "user": {
                "login": author_login,
                "id": 20000 + hash(author_login) % 10000,
                "type": "User"
            },
            "state": state,
            "created_at": iso_created,
            "updated_at": closed_at if closed_at else iso_created,
            "closed_at": closed_at,
            "labels": labels,
            "linked_pulls": pull_links,
            "comments": comments
        }
        issues.append(issue_obj)

        # Write issue fixture
        with open(os.path.join(issues_dir, f"{iss_num}.json"), "w", encoding="utf-8") as f:
            json.dump(issue_obj, f, indent=2)

        # Append to events
        events.append({
            "event": "issues.opened",
            "timestamp": iso_created,
            "actor": author_login,
            "issue_number": iss_num,
            "data": {"title": title, "labels": labels}
        })
        if closed_at:
            events.append({
                "event": "issues.closed",
                "timestamp": closed_at,
                "actor": author_login,
                "issue_number": iss_num,
                "data": {"state": "closed"}
            })

    # Synchronize PR bodies with Fixes #N
    print("Synchronizing PR bodies with Fixes #N for linked issues...")
    for iss_num, pr_list in linked_pairs.items():
        for pnum in pr_list:
            p_file = os.path.join(pulls_dir, f"{pnum}.json")
            if os.path.exists(p_file):
                with open(p_file, "r", encoding="utf-8") as f:
                    pr_data = json.load(f)
                keyword = "Fixes" if pnum % 2 == 0 else "Closes"
                if f"#{iss_num}" not in pr_data["body"]:
                    pr_data["body"] = f"{pr_data['body']}\n\n{keyword} #{iss_num}"
                    with open(p_file, "w", encoding="utf-8") as f:
                        json.dump(pr_data, f, indent=2)

    # Re-save events.jsonl
    events.sort(key=lambda x: x["timestamp"])
    with open(events_path, "w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")

    print(f"Generated {len(issues)} issues in {issues_dir}")
    print(f"Generated {total_issue_comments} issue comments (Target: 1,000+)")
    print(f"Linked issues: {len([i for i in issues if i['linked_pulls']])} ({len([i for i in issues if i['linked_pulls']])/len(issues)*100:.1f}%)")
    print(f"Total events in stream: {len(events)}")
    return issues

if __name__ == "__main__":
    run()
