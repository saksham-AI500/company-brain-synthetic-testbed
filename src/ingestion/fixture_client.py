"""
GitHub Fixture Client for RepoBrain Ingestion Layer.
Reads synthetic fixtures through the same normalized API code path as live GitHub REST API v3.
"""
import os
import json
import glob
from typing import Dict, Any, List, Optional

class GitHubFixtureClient:
    def __init__(self, fixtures_dir: str = "data/synthetic/fixtures"):
        self.fixtures_dir = fixtures_dir
        self.pulls_dir = os.path.join(fixtures_dir, "pulls")
        self.issues_dir = os.path.join(fixtures_dir, "issues")

    def get_repository(self) -> Dict[str, Any]:
        p = os.path.join(self.fixtures_dir, "repository.json")
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_pull(self, number: int) -> Dict[str, Any]:
        p = os.path.join(self.pulls_dir, f"{number}.json")
        if not os.path.exists(p):
            raise FileNotFoundError(f"Pull request #{number} not found in fixtures.")
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_pulls(self, state: str = "all", per_page: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        all_pulls = []
        files = sorted(glob.glob(os.path.join(self.pulls_dir, "*.json")), key=lambda x: int(os.path.basename(x).split(".")[0]))
        for f in files:
            with open(f, "r", encoding="utf-8") as pf:
                data = json.load(pf)
                if state == "all" or data.get("state") == state:
                    all_pulls.append(data)
        
        start = (page - 1) * per_page
        end = start + per_page
        return all_pulls[start:end]

    def get_issue(self, number: int) -> Dict[str, Any]:
        p = os.path.join(self.issues_dir, f"{number}.json")
        if not os.path.exists(p):
            raise FileNotFoundError(f"Issue #{number} not found in fixtures.")
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_issues(self, state: str = "all", per_page: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        all_issues = []
        files = sorted(glob.glob(os.path.join(self.issues_dir, "*.json")), key=lambda x: int(os.path.basename(x).split(".")[0]))
        for f in files:
            with open(f, "r", encoding="utf-8") as pf:
                data = json.load(pf)
                if state == "all" or data.get("state") == state:
                    all_issues.append(data)

        start = (page - 1) * per_page
        end = start + per_page
        return all_issues[start:end]

    def list_reviews(self, pull_number: int) -> List[Dict[str, Any]]:
        pr = self.get_pull(pull_number)
        return pr.get("reviews", [])

    def list_comments(self, pull_number: int) -> List[Dict[str, Any]]:
        pr = self.get_pull(pull_number)
        return pr.get("comments", [])

    def list_events(self, per_page: int = 50, page: int = 1) -> List[Dict[str, Any]]:
        events_path = os.path.join(self.fixtures_dir, "events.jsonl")
        events = []
        if os.path.exists(events_path):
            with open(events_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        start = (page - 1) * per_page
        end = start + per_page
        return events[start:end]

def normalize_pull_request(raw_pr: Dict[str, Any]) -> Dict[str, Any]:
    """Normalized schema representation used by graph sync engine."""
    return {
        "id": raw_pr["id"],
        "number": raw_pr["number"],
        "title": raw_pr["title"],
        "body": raw_pr["body"],
        "author": raw_pr["user"]["login"],
        "state": raw_pr["state"],
        "created_at": raw_pr["created_at"],
        "closed_at": raw_pr.get("closed_at"),
        "merged_at": raw_pr.get("merged_at"),
        "is_merged": raw_pr.get("merged_at") is not None,
        "files": [f["filename"] for f in raw_pr.get("files", [])],
        "reviews_count": len(raw_pr.get("reviews", [])),
        "comments_count": len(raw_pr.get("comments", []))
    }

def normalize_issue(raw_issue: Dict[str, Any]) -> Dict[str, Any]:
    """Normalized schema representation used by graph sync engine."""
    return {
        "id": raw_issue["id"],
        "number": raw_issue["number"],
        "title": raw_issue["title"],
        "body": raw_issue["body"],
        "author": raw_issue["user"]["login"],
        "state": raw_issue["state"],
        "created_at": raw_issue["created_at"],
        "closed_at": raw_issue.get("closed_at"),
        "labels": raw_issue.get("labels", []),
        "linked_pulls": raw_issue.get("linked_pulls", []),
        "comments_count": len(raw_issue.get("comments", []))
    }
