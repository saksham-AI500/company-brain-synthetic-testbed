"""
Master deterministic synthetic data generator for Acme Platform Inc.
Usage:
  python scripts/generate_synthetic.py --stage 1
  python scripts/generate_synthetic.py --stage 2
  ...
  python scripts/generate_synthetic.py --all
"""
import os
import sys
import json
import yaml
import shutil
import hashlib
from datetime import datetime

SEED = 20260930

def load_plan():
    plan_path = os.path.join("data", "synthetic", "PLAN.yaml")
    if not os.path.exists(plan_path):
        raise FileNotFoundError(f"Plan not found at {plan_path}. Run build_plan.py first.")
    with open(plan_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_stage_1():
    print("=== RUNNING STAGE 1: People, Teams, and CODEOWNERS ===")
    plan = load_plan()
    fixtures_dir = os.path.join("data", "synthetic", "fixtures")
    os.makedirs(fixtures_dir, exist_ok=True)
    os.makedirs(".github", exist_ok=True)

    # 1. people.json
    people = []
    for p in plan["roster"]:
        person_obj = {
            "login": p["login"],
            "name": p["name"],
            "email": f"{p['login']}@example.com",
            "team": p["team"],
            "role": p["role"],
            "group": p["group"],
            "start_date": p["start_date"],
            "end_date": p["end_date"],
            "is_bot": (p["group"] == "bot"),
            "review_strength": p["review_strength"],
            "reviews_per_week": p["reviews_per_week"],
            "out_of_office": p.get("out_of_office"),
            "timezone": p.get("timezone", "UTC")
        }
        people.append(person_obj)

    people_path = os.path.join(fixtures_dir, "people.json")
    with open(people_path, "w", encoding="utf-8") as f:
        json.dump(people, f, indent=2)
    print(f"Wrote {len(people)} people to {people_path}")

    # 2. teams.json
    teams = []
    for t in plan["teams"]:
        members = [p["login"] for p in plan["roster"] if p["team"] == t["handle"]]
        team_obj = {
            "handle": t["handle"],
            "name": t["name"],
            "target_count": t["target_count"],
            "members": members,
            "senior_reviewers": t["senior_reviewers"],
            "primary_modules": t["primary_modules"]
        }
        teams.append(team_obj)

    teams_path = os.path.join(fixtures_dir, "teams.json")
    with open(teams_path, "w", encoding="utf-8") as f:
        json.dump(teams, f, indent=2)
    print(f"Wrote {len(teams)} teams to {teams_path}")

    # 3. repository.json
    repo_obj = {
        "id": 901234567,
        "name": "company-brain-synthetic-testbed",
        "full_name": "saksham-AI500/company-brain-synthetic-testbed",
        "html_url": "https://github.com/saksham-AI500/company-brain-synthetic-testbed",
        "description": "Deterministic synthetic company testbed for RepoBrain (Acme Platform Inc.)",
        "private": False,
        "owner": {
            "login": "acme-platform",
            "type": "Organization"
        },
        "default_branch": "main",
        "created_at": "2025-10-01T00:00:00Z",
        "updated_at": "2026-09-30T23:59:59Z",
        "pushed_at": "2026-09-30T23:59:59Z",
        "open_issues_count": 35,
        "license": {
            "key": "mit",
            "name": "MIT License"
        }
    }
    repo_path = os.path.join(fixtures_dir, "repository.json")
    with open(repo_path, "w", encoding="utf-8") as f:
        json.dump(repo_obj, f, indent=2)
    print(f"Wrote repository fixture to {repo_path}")

    # 4. CODEOWNERS and codeowners.txt
    lines = [
        "# CODEOWNERS for Acme Platform Inc.",
        "# Lines starting with '#' are comments.",
        "# Syntax: pattern [owners...]",
        ""
    ]
    for rule in plan["codeowners_rules"]:
        owners_str = " ".join(rule["owners"])
        lines.append(f"{rule['pattern']} {owners_str}")
    codeowners_content = "\n".join(lines) + "\n"

    codeowners_txt_path = os.path.join(fixtures_dir, "codeowners.txt")
    with open(codeowners_txt_path, "w", encoding="utf-8") as f:
        f.write(codeowners_content)

    with open("CODEOWNERS", "w", encoding="utf-8") as f:
        f.write(codeowners_content)

    with open(os.path.join(".github", "CODEOWNERS"), "w", encoding="utf-8") as f:
        f.write(codeowners_content)
    print(f"Wrote CODEOWNERS with {len(plan['codeowners_rules'])} rules")

    # Validate stage 1
    assert len(people) == 56, f"Expected 56 people, got {len(people)}"
    group_counts = {}
    for p in people:
        g = p["group"]
        group_counts[g] = group_counts.get(g, 0) + 1
    assert group_counts == {"current": 44, "former": 5, "contractor": 3, "bot": 4}, f"Unexpected group split: {group_counts}"
    assert len(teams) == 4, f"Expected 4 teams, got {len(teams)}"
    assert len(plan["codeowners_rules"]) >= 25, "Expected >=25 CODEOWNERS rules"
    print("Stage 1 validation checks PASSED successfully!\n")

def run_stage_2():
    print("=== RUNNING STAGE 2: Modules and Files ===")
    from scripts.generate_codebase import build_all_files
    files = build_all_files()
    print(f"Stage 2 complete: generated and compiled {len(files)} files.\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--stage" in args:
        idx = args.index("--stage")
        stage = args[idx + 1]
        if stage == "1":
            run_stage_1()
        elif stage == "2":
            run_stage_2()
        else:
            print(f"Stage {stage} not yet implemented in standalone caller.")
    else:
        run_stage_1()
        run_stage_2()
