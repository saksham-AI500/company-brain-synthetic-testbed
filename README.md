# company-brain-synthetic-testbed

Deterministic synthetic repository and benchmark dataset for company-brain knowledge retrieval, code intelligence, and team dynamics analysis.

## Overview

- **Repository**: `saksham-AI500/company-brain-synthetic-testbed`
- **Target Organization**: Acme Platform Inc.
- **Seed**: `20260930`
- **Target Dataset SHA-256**: `a221cb67d0c64344d8aae878fa2f7a60a39dc400b954c6ba324e6aabaeb46e41`
- **Time Horizon**: October 1, 2025 to September 30, 2026 (12 months)

## Synthetic Data

> [!IMPORTANT]
> **Fixtures are Authoritative**: The local fixtures located in `data/synthetic/fixtures/` (`pulls/`, `issues/`, `events.jsonl`, `people.json`, `teams.json`, `ground_truth.json`) are the primary source of truth for all evaluation benchmarks, ground truth timestamps, and entity schemas.
>
> **Single-Account Provenance**: Because GitHub requires authentication to write issues, pull requests, and reviews, all GitHub pull requests and reviews are created and submitted by `@saksham-AI500`. Fictional identities (such as Acme engineers, team leads, and contractors) are preserved with their original fictional email addresses (`@example.com`) in the commit history (using `GIT_AUTHOR_DATE`, `GIT_COMMITTER_DATE`, and author metadata) and explicitly attributed in each pull request description, review body, and comment. The exact fictional reviewer mappings and ground truth scenarios are documented in `data/synthetic/ground_truth.json`.

## Repository Structure

- `data/synthetic/fixtures/`: Complete JSON fixtures for 720 PRs, 350 issues, 56 people, 4 teams, and 3,103 events.
- `data/synthetic/MANIFEST.json`: Verified entity counts and dataset hash.
- `data/synthetic/ground_truth.json`: 20 evaluation benchmark questions and 8 scenario ground-truth answers.
- `project_context/`: Master prompt documentation, context specifications, and push progress checkpoints.
- `docs/`: Engineering architecture, RFCs, runbooks, and onboardings.
- `scripts/`: Generation, validation, and push automation tooling.
- `src/` & microservice modules: Full multi-service source code across 14 modules.