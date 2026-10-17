"""
Change script for Acme Platform Inc. (keeping knowledge current demo).
Usage:
  python scripts/apply_changes.py --step 1
  python scripts/apply_changes.py --step 2
  python scripts/apply_changes.py --step 3
"""
import os
import sys
import json
import argparse
from datetime import datetime

def get_changes_dir():
    d = os.path.join("data", "synthetic", "changes")
    os.makedirs(d, exist_ok=True)
    return d

def apply_step_1():
    print("Applying Step 1: Reassign search/ ownership in CODEOWNERS from @acme/growth to @acme/platform...")
    changes_dir = get_changes_dir()
    step_file = os.path.join(changes_dir, "step_1.json")

    codeowners_paths = ["CODEOWNERS", os.path.join(".github", "CODEOWNERS"), os.path.join("data", "synthetic", "fixtures", "codeowners.txt")]
    modified_files = []

    for cp in codeowners_paths:
        if os.path.exists(cp):
            with open(cp, "r", encoding="utf-8") as f:
                content = f.read()
            if "search/ @acme/growth" in content:
                new_content = content.replace("search/ @acme/growth", "search/ @acme/platform")
                with open(cp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                modified_files.append(cp)

    change_record = {
        "step": 1,
        "description": "Reassign search/ ownership in CODEOWNERS from @acme/growth to @acme/platform",
        "timestamp": datetime.now().isoformat(),
        "changes": [
            {
                "file": "CODEOWNERS",
                "pattern": "search/",
                "old_owners": ["@acme/growth"],
                "new_owners": ["@acme/platform"]
            }
        ],
        "modified_files": modified_files,
        "idempotent": True
    }

    with open(step_file, "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)

    # Also keep a copy at changes/step_1.json if needed
    os.makedirs("changes", exist_ok=True)
    with open(os.path.join("changes", "step_1.json"), "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)

    print(f"Step 1 applied and recorded in {step_file}\n")
    return change_record

def apply_step_2():
    print("Applying Step 2: Close issue #78 and add review by current employee to PR #650...")
    changes_dir = get_changes_dir()
    step_file = os.path.join(changes_dir, "step_2.json")

    # 1. Close issue #78
    issue_path = os.path.join("data", "synthetic", "fixtures", "issues", "78.json")
    old_issue_state = "open"
    if os.path.exists(issue_path):
        with open(issue_path, "r", encoding="utf-8") as f:
            issue_data = json.load(f)
        old_issue_state = issue_data.get("state", "open")
        issue_data["state"] = "closed"
        issue_data["closed_at"] = "2026-09-25T14:00:00Z"
        with open(issue_path, "w", encoding="utf-8") as f:
            json.dump(issue_data, f, indent=2)

    # 2. Add review by current employee (Devon Reed) to PR #650
    pr_path = os.path.join("data", "synthetic", "fixtures", "pulls", "650.json")
    review_added = False
    if os.path.exists(pr_path):
        with open(pr_path, "r", encoding="utf-8") as f:
            pr_data = json.load(f)
        existing_logins = [r["user"]["login"] for r in pr_data.get("reviews", [])]
        if "devon-reed" not in existing_logins:
            new_review = {
                "id": 65005,
                "user": {"login": "devon-reed", "type": "User"},
                "body": "Reviewed trace sampling configuration. Approved per observability standards.",
                "state": "APPROVED",
                "submitted_at": "2026-09-25T15:30:00Z",
                "html_url": "https://github.com/saksham-AI500/company-brain-synthetic-testbed/pull/650#pullrequestreview-65005"
            }
            pr_data.setdefault("reviews", []).append(new_review)
            with open(pr_path, "w", encoding="utf-8") as f:
                json.dump(pr_data, f, indent=2)
            review_added = True

    change_record = {
        "step": 2,
        "description": "Close issue #78 and add review by current employee (devon-reed) to PR #650",
        "timestamp": datetime.now().isoformat(),
        "changes": [
            {"target": "issue:78", "old_state": old_issue_state, "new_state": "closed"},
            {"target": "pull:650", "review_added": review_added, "reviewer": "devon-reed"}
        ],
        "idempotent": True
    }

    with open(step_file, "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)
    with open(os.path.join("changes", "step_2.json"), "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)

    print(f"Step 2 applied and recorded in {step_file}\n")
    return change_record

def apply_step_3():
    print("Applying Step 3: Remove function reconcile_unsettled_batches from payments/refunds/batch.py...")
    changes_dir = get_changes_dir()
    step_file = os.path.join(changes_dir, "step_3.json")

    batch_py = os.path.join("payments", "refunds", "batch.py")
    removed = False
    if os.path.exists(batch_py):
        with open(batch_py, "r", encoding="utf-8") as f:
            code = f.read()
        if "def reconcile_unsettled_batches" in code:
            lines = code.splitlines()
            new_lines = []
            skip = False
            for line in lines:
                if "def reconcile_unsettled_batches" in line:
                    skip = True
                    removed = True
                    continue
                if skip and line.startswith("def "):
                    skip = False
                if not skip:
                    new_lines.append(line)
            with open(batch_py, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines) + "\n")

    change_record = {
        "step": 3,
        "description": "Removed reconcile_unsettled_batches() from payments/refunds/batch.py, making payment-pipeline-recovery.md stale",
        "timestamp": datetime.now().isoformat(),
        "changes": [
            {
                "file": "payments/refunds/batch.py",
                "removed_function": "reconcile_unsettled_batches",
                "stale_document": "docs/runbooks/payment-pipeline-recovery.md"
            }
        ],
        "idempotent": True
    }

    with open(step_file, "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)
    with open(os.path.join("changes", "step_3.json"), "w", encoding="utf-8") as f:
        json.dump(change_record, f, indent=2)

    print(f"Step 3 applied and recorded in {step_file}\n")
    return change_record

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply synthetic change script steps")
    parser.add_argument("--step", type=int, choices=[1, 2, 3], required=True, help="Step number (1, 2, or 3)")
    args = parser.parse_args()

    if args.step == 1:
        apply_step_1()
    elif args.step == 2:
        apply_step_2()
    elif args.step == 3:
        apply_step_3()
