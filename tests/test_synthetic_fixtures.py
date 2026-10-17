"""
Tests showing existing ingestion code reads synthetic fixtures through same code path as live GitHub API.
"""
import pytest
from src.ingestion.fixture_client import (
    GitHubFixtureClient,
    normalize_pull_request,
    normalize_issue
)

@pytest.fixture
def client():
    return GitHubFixtureClient()

def test_client_get_repository(client):
    repo = client.get_repository()
    assert repo["name"] == "company-brain-synthetic-testbed"
    assert "owner" in repo
    assert repo["owner"]["login"] == "acme-platform"

def test_client_pull_requests(client):
    # Fetch first page of pulls
    pulls = client.list_pulls(per_page=10, page=1)
    assert len(pulls) == 10
    pr1 = client.get_pull(1)
    assert pr1["number"] == 1
    assert "title" in pr1
    assert "user" in pr1
    assert "files" in pr1
    assert "reviews" in pr1

    # Check normalized structure
    norm = normalize_pull_request(pr1)
    assert norm["number"] == 1
    assert isinstance(norm["files"], list)
    assert isinstance(norm["reviews_count"], int)

def test_client_issues(client):
    issues = client.list_issues(per_page=10, page=1)
    assert len(issues) == 10
    issue42 = client.get_issue(42)
    assert issue42["number"] == 42
    assert "Checkout timeout" in issue42["title"]
    assert 145 in issue42["linked_pulls"]

    norm_issue = normalize_issue(issue42)
    assert norm_issue["number"] == 42
    assert 145 in norm_issue["linked_pulls"]

def test_client_event_stream(client):
    events = client.list_events(per_page=50, page=1)
    assert len(events) == 50
    for ev in events:
        assert "event" in ev
        assert "timestamp" in ev
        assert "actor" in ev

def test_planted_pull_scenarios(client):
    # Verify planted PR #205 (R2 exact tie)
    pr205 = client.get_pull(205)
    reviewers = [r["user"]["login"] for r in pr205["reviews"]]
    assert "caleb-rivers" in reviewers
    assert "clara-oswald" in reviewers

    # Verify planted PR #215 (Q12 decision comment)
    pr215 = client.get_pull(215)
    bodies = [r["body"] for r in pr215["reviews"]]
    assert any("We are going with per-tenant rate limits." in b for b in bodies)
