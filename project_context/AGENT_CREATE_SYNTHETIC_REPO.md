# PROMPT: Create the Synthetic Company Repo in My GitHub Repository

Paste this whole file to your coding agent. It replaces the "wait for an answer" steps in `AGENT_READ_AND_EXECUTE.md` with decisions, so you can run it end to end. Save a copy as `project_context/AGENT_CREATE_SYNTHETIC_REPO.md`.

---

## Target repository

**My repo URL:** `https://github.com/saksham-AI500/company-brain-synthetic-testbed`


Rules for the target:
- It must be a **separate, empty, public repository** owned by me. Do not use the RepoBrain project repository. Filling the project repo with 800 synthetic PRs would make the project history look fake and would conflict with the rule that our timeline must be truthful.
- If the URL points to the RepoBrain repo, stop and ask me to confirm before doing anything.
- If the repo is not empty, stop and ask me.

Local layout: the fixtures in `data/synthetic/` are the source of truth. The GitHub repo is the rendered, pushed copy of the company's code and history.

---

## Decisions for the open questions

These answer the questions you raised in `SPEC_UNDERSTANDING.md`. Use them. Do not ask again.

**1. Roster mapping (44 + 5 + 1 = 50 team members).**
- The four team rosters total 50 people: 44 current employees, 5 former employees, and 1 contractor. Platform 14, Payments 13, Identity 11, Growth 12.
- The other 2 contractors are external. Each is attached to one module as a contractor, with no team handle.
- The 4 bots have no team. They appear as reviewers only.
- Senior reviewer counts per team stay as the addendum says.

**2. Question prompts Q1 to Q20.**
- `AGENT_BRIEF.md` is not in the repo. Write the 20 questions yourself, using the list in the brief's section on the 20 questions (groups A to E, with the (T) sealed-test marks), and store them in `ground_truth.json`. The wording in this brief is the one to use.
- Q2, Q13, and Q15 need planted facts too. Add them:
  - Q2: an open issue on the auth-token migration that is linked to a doc in `docs/`.
  - Q13: a CODEOWNERS change in step 1 of the change script (`search/` moves owners).
  - Q15: a CODEOWNERS mismatch in `payments/` for the CODEOWNERS patch draft.

**3. R2 tie formula.** Use this formula everywhere the system ranks reviewers:

```
score(person, module, as_of) =
    round(
      0.7 * review_strength[module]
    + 0.3 * min(1.0, reviews_in_module_last_90d / 10)
    - 0.05 * open_review_requests,
    3)
```

- `reviews_in_module_last_90d` counts reviews by the person on PRs that touch the module, submitted in the 90 days before `as_of`.
- `open_review_requests` is the count of PRs where the person is a requested reviewer and has not yet reviewed, as of `as_of`. Use 0 for all planted tie cases unless the scenario says otherwise.
- Ties: when two scores are equal at 3 decimals, rank by login, alphabetically. For R2, plant two people with identical inputs so the score is exactly equal, and record both in `ground_truth.json` as a tie.
- Excluded from ranking: bots, former employees after `end_date`, people on leave, the PR author.

**4. Ingestion test.** Yes, create a reference fixture reader in `src/ingestion/fixture_client.py` that exposes the same methods and return shapes as the live GitHub client. Then `tests/test_synthetic_fixtures.py` checks that both clients produce the same normalized records for a sample of PRs. If the live client already exists in the repo, match its signatures. If not, document the expected shape in the test.

**5. Git.** Yes. Clone my empty repo and commit into it. Each stage gets its own commit, backdated as the spec says. Do not force-push. If a push fails, stop and report the error.

---

## Build sequence

Run these in order. Pause only where marked.

1. **Setup.** Clone my repo. Create `data/synthetic/`. Write `SPEC_UNDERSTANDING.md` with the decisions above applied.
2. **PLAN gate (pause).** Write `data/synthetic/PLAN.yaml` (56 people, 14 modules, CODEOWNERS, planted facts Q1 to Q20, scenarios R1 to R8, counts). Show it to me. **Wait for my "approved" before continuing.**
3. **Generate fixtures locally** in stages (people and CODEOWNERS; files; PRs in date order; issues and comments; docs; planted facts and distractors; change script). Validate after each stage and commit to my repo with a stage message.
4. **Validate.** Run `scripts/validate_dataset.py`. Paste its real output into `VALIDATION_REPORT.md`. Include the 56-person table.
5. **Push to my GitHub repo.** Use one commit per PR (or per batch of PRs), backdated. Open PRs from branches, add reviews from the token owner, and merge where the plan says so. Rate limits: keep under about 80 content-creating requests per minute, sleep between batches, retry on secondary-limit 403 responses with backoff.
6. **Verify the live repo.** Re-count PRs, issues, and commits on GitHub and compare against `MANIFEST.json`. Paste the output.
7. **Report.** Give me the repo URL, the counts, the SHA-256, the tier reached, and anything not done.

---

## Important: what GitHub can and cannot show

GitHub attributes every PR and review to the account whose token created it. My token is one account, so on the live repo:
- All PRs will show as opened by my account.
- Reviews will show my account, not the 56 fictional people.
- Fictional people appear in commit author fields (`git -c user.name=... -c user.email=...@example.com`) and in the fixtures.

Put this in the repo's `README.md` under a "Synthetic data" heading, and say that the fixtures in `data/synthetic/` are the authoritative roster. Do not try to create extra GitHub accounts to fix this, and do not use `Co-authored-by` to fake reviews.

---

## Rules

- Never print, log, or commit my token. Read it from `.env`. If it is missing, stop and ask me to add it.
- Never create GitHub accounts. Never copy text from real repositories or from the FalkorDB repo.
- Fictional names only. All emails use `example.com`. Fake tokens are marked `FAKE_TOKEN_DO_NOT_USE`.
- Do not claim "all checks pass" unless the validation script printed it.
- If something cannot be done, stop and report it. Do not pad the data to hit a number.
- Tell me the AI tool and model you used, for the AI disclosure.
