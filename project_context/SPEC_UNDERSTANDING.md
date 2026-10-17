# Specification Understanding: Synthetic Company Dataset for RepoBrain

## Goal
Build a deterministic synthetic data generator creating a realistic 12-month engineering history for "Acme Platform Inc." (56-person roster, 14 modules, CODEOWNERS, 600–800 PRs, 350 issues, docs, and planted ground-truth facts/review scenarios) to test and evaluate the RepoBrain knowledge graph.

---

## Scale I will target
Entity counts after applying the addendum (`PEOPLE_EXPANSION.md`) and user decisions (`AGENT_CREATE_SYNTHETIC_REPO.md`):

- **Time span:** 12 months ending 2026-09-30 (weekday-heavy, realistic sprint cycles).
- **People (Total 56 fixture records):**
  - **44** Current human employees across 4 teams
  - **5** Former employees (left mid-period; zero activity after `end_date`) assigned to teams
  - **3** Contractors: 1 internal team-affiliated contractor + 2 external contractors attached to a single module with no team handle
  - **4** Bots (`ci-review-bot[bot]`, `dependency-bot[bot]`, `security-scan[bot]`, `docs-lint[bot]`) with no team handle, appearing as reviewers only
- **Teams (4 teams totaling 50 affiliated members = 44 current + 5 former + 1 contractor):**
  - `@acme/platform`: 14 members, 3 senior reviewers (2+ reviews/week) | Primary: `infra/deploy/`, `infra/observability/`, `api/gateway/`, `shared/utils/`
  - `@acme/payments`: 13 members, 3 senior reviewers (2+ reviews/week) | Primary: `payments/`, `payments/refunds/`, `billing/`
  - `@acme/identity`: 11 members, 2 senior reviewers (2+ reviews/week) | Primary: `auth/`, `auth/mfa/`
  - `@acme/growth`: 12 members, 2 senior reviewers (2+ reviews/week) | Primary: `search/`, `search/indexer/`, `notifications/`, `growth/experiments/`, `growth/referrals/`
- **Modules (14):**
  - `auth/`, `auth/mfa/`, `payments/`, `payments/refunds/`, `billing/`, `search/`, `search/indexer/`, `notifications/`, `growth/experiments/`, `growth/referrals/`, `infra/deploy/`, `infra/observability/`, `api/gateway/`, `shared/utils/`
- **Declared Ownership (CODEOWNERS):**
  - 25+ rules with nested overrides, at least 2 stale team handles, at least 2 unowned modules, and 1 non-existent team handle.
- **Repository Files:**
  - ~350 files (valid Python source files passing `python -m py_compile`, valid JSON/YAML configs, markdown docs, tests).
- **Pull Requests:**
  - 600 to 800 PRs (merged, closed-unmerged, open; reviews on at least 85% of merged PRs).
- **Commits:**
  - At least 2,000 commits (multiple commits per PR, squash & merge commits, backdated `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` in chronological order).
- **Issues:**
  - 350 issues (bugs, features, incidents; 40% linked to PRs via explicit `Fixes #N` or `Closes #N`).
- **Comments:**
  - 3,000+ review comments and PR comments.
  - 1,000+ issue comments.
- **Documents:**
  - 45 markdown files: 12 ADRs, 10 runbooks, 14 module READMEs, 9 onboarding & contributing guides (all with explicit `#123` references and path links).
- **Decisions:**
  - 25 explicit decisions across ADRs, issues, and PR comments.
- **Ground Truth Evaluation:**
  - 20 evaluation questions (Q1–Q20) mapped to planted facts (Groups A–E).
  - 8 reviewer query scenarios (R1–R8) stored separately in `ground_truth.json`.
  - At least 20 distractor facts.
- **Change Script:**
  - `scripts/apply_changes.py` with 3 idempotent steps outputting `changes/step_1.json`, `changes/step_2.json`, and `changes/step_3.json`.
- **Ingestion Test & Validation:**
  - Fixtures in `data/synthetic/fixtures/` matching GitHub REST API shape.
  - Reference client in `src/ingestion/fixture_client.py` and tests in `tests/test_synthetic_fixtures.py`.
  - Combined `scripts/validate_dataset.py` running all Checks 1–10 plus Addendum Checks.
  - `VALIDATION_REPORT.md` containing real command outputs and full 56-person table.

---

## Overrides
Places where the Addendum (`PEOPLE_EXPANSION.md`) overrides the Main Spec (`SYNTHETIC_DATA_PROMPT.md`):

| Topic | Main Spec (`SYNTHETIC_DATA_PROMPT.md`) | Addendum (`PEOPLE_EXPANSION.md`) | Effective Value to Use |
|---|---|---|---|
| **Total People** | 28 people (22 current, 2 former, 1 contractor, 2 bots) | 56 people (44 current, 5 former, 3 contractors, 4 bots) | **56 people** |
| **Team Sizes & Reviewers** | 4 teams, ~12 people each (approximate) | 4 teams: Platform (14, 3 sr), Payments (13, 3 sr), Identity (11, 2 sr), Growth (12, 2 sr) | **Addendum team specifications** |
| **Person Metadata Schema** | `login`, `name`, `team`, `role`, `start_date`, `end_date`, `is_bot`, `expertise_tags` | Adds: `review_strength` (0.0–1.0 per module), `reviews_per_week` (senior: 2–6, mid: 0.5–2, junior: 0–0.5), `out_of_office` (`{start, end}`), `timezone` | **Addendum expanded schema** |
| **Bot Accounts** | 2 bots (`ci-review-bot[bot]`, `dependency-bot[bot]`) | 4 bots (`ci-review-bot[bot]`, `dependency-bot[bot]`, `security-scan[bot]`, `docs-lint[bot]`) | **4 bots** |
| **Review Distribution & Limits** | One senior reviewer reviews 40% of platform PRs | No single human reviews >25% of all PRs; >=12 people review in `auth/` or `payments/`; >=6 inactive in last 90d; >=4 cross-team reviewers; strict zero self-reviews | **Addendum review distribution constraints** |
| **Ground Truth Questions** | Q1 to Q20 | Adds R1 to R8 reviewer scenarios (stored separately in `ground_truth.json`) | **Both (Q1–Q20 and R1–R8)** |
| **Validation Checks** | Checks 1 to 10 | Adds checks for 56 count/group split, `end_date` enforcement, self-review prohibition, 25% max concentration, R1–R8 scenario presence, and R2 exact score tie verification | **Combined validation suite** |
| **Reporting Requirements** | Standard validation report | Adds detailed people table (login, team, role, group, 90d reviews, 12m reviews, modules) to `VALIDATION_REPORT.md` | **Addendum reporting specification** |

---

## Hard constraints
Rules that must never be broken:

1. **Deterministic seed:** Default seed `20260930`. Identical seed MUST reproduce byte-identical output with matching SHA-256 recorded in `data/synthetic/MANIFEST.json`.
2. **No real people:** All names must be fictional and checked against a blocklist of public figures; all emails must strictly use `@example.com`.
3. **No fake GitHub accounts:** Do not create real or fake GitHub accounts. The 56 persons exist purely as fixture JSON records and commit authors (`git -c user.name=... -c user.email=...`).
4. **No copied text:** No copying text from real repositories, real docs, or FalkorDB. All source code, PR/issue comments, ADRs, and guides must be generated programmatically.
5. **No real secrets:** Never print, log, or commit tokens or keys. Read them from `.env`. Any token strings in test fixtures must be explicitly marked fake (e.g., `FAKE_TOKEN_DO_NOT_USE`).
6. **Realistic, compilable code:** Generated Python files must compile cleanly with `python -m py_compile`; JSON and YAML configs must parse without errors.
7. **Strict chronology & timeline:** All events within the 12-month window ending 2026-09-30. Reviews must strictly follow PR open time. No activity occurs for any person after their `end_date`. Git timestamps backdated and ordered.
8. **Planted facts integrity:** All planted facts (Q1–Q20) and review scenarios (R1–R8) must exist in data and ground truth before generation; distractors must be included and marked.
9. **Approval gate:** `PLAN.yaml` must be created, shown, and approved before generating the dataset.

---

## Applied Decisions
All open questions have been resolved per `AGENT_CREATE_SYNTHETIC_REPO.md`:

1. **Roster breakdown:**
   - 4 teams total 50 members: 44 current human employees, 5 former employees, 1 contractor. (Platform: 14, Payments: 13, Identity: 11, Growth: 12).
   - 2 external contractors have no team handle, each attached to one module.
   - 4 bots have no team handle, appear as reviewers only.
   - Senior reviewer counts: Platform 3, Payments 3, Identity 2, Growth 2.
2. **Question prompts Q1–Q20:**
   - Grouped A–E with (T) sealed-test marks.
   - Planted facts include:
     - Q2: an open issue on auth-token migration linked to a doc in `docs/`.
     - Q13: a CODEOWNERS change in step 1 of the change script (`search/` moves owners from growth to platform).
     - Q15: a CODEOWNERS mismatch in `payments/` for the CODEOWNERS patch draft.
     - Full set Q1–Q20 mapped with exact questions, expected answers, source IDs, forbidden answers, and should_refuse flags.
3. **Reviewer scoring formula for R2 tie:**
   $$\text{score}(p, m, \text{as\_of}) = \text{round}(0.7 \times \text{review\_strength}[m] + 0.3 \times \min(1.0, \text{reviews\_in\_module\_last\_90d} / 10) - 0.05 \times \text{open\_review\_requests}, 3)$$
   - Ties broken alphabetically by login. For R2, plant two candidates with identical inputs so their score is identical to 3 decimals, and record both as a tie.
   - Exclusions: bots, former employees after `end_date`, employees on leave during PR date, and PR author.
4. **Ingestion client & test:**
   - Create `src/ingestion/fixture_client.py` providing normalized GitHub API endpoints.
   - `tests/test_synthetic_fixtures.py` verifies parsing consistency against fixtures.
5. **Git repository:**
   - Workspace linked to `https://github.com/saksham-AI500/company-brain-synthetic-testbed`. Each stage will be committed locally with stage commit messages.
