# PROMPT: How to Read and Execute the Synthetic Data Specs

Paste this whole file to your coding agent first. It tells the agent how to read the two specs, which one wins when they disagree, and what to do in what order. Save a copy as `project_context/AGENT_READ_AND_EXECUTE.md`.

Specs (both must be in the repo under `project_context/`):
1. `SYNTHETIC_DATA_PROMPT.md`: the main task (scale, constraints, ground truth, change script, outputs, validation)
2. `PEOPLE_EXPANSION.md`: an addendum that overrides the people section of the main spec

---

## Step 1: Read both files completely before writing any code

Read `SYNTHETIC_DATA_PROMPT.md` first, then `PEOPLE_EXPANSION.md`. Do not skim. Then write a short summary of your understanding in `project_context/SPEC_UNDERSTANDING.md` with these headings:

- **Goal:** one sentence
- **Scale I will target:** entity counts after applying the addendum
- **Overrides:** every place where the addendum changes the main spec, and the new value
- **Hard constraints:** the rules I must never break (deterministic seed, no real people, no fake GitHub accounts, no copied text, no secrets)
- **Open questions:** anything ambiguous; do not guess, ask me

Show me this file and wait for my reply before continuing.

## Step 2: Apply the override rules

These rules decide which spec wins when they conflict:

| Topic | Main spec says | Addendum says | Use |
|---|---|---|---|
| Total people | 28 | 56 (44 current, 5 former, 3 contractors, 4 bots) | **56** |
| Teams | 4 teams, 12 people each (approximate) | 4 teams, 9 to 14 each, with senior reviewer counts | **Addendum** |
| GitHub accounts | Do not create 28 real accounts | Do not create any new accounts | **Both: no new accounts** |
| Reviewer ground truth | Q1 to Q20 | Adds R1 to R8 | **Both** (store R1 to R8 separately in `ground_truth.json`) |
| Validation | Checks 1 to 10 | Adds self-review, concentration, tie, and person-count checks | **Both** (combine into one `validate_dataset.py`) |

If a conflict is not in this table, stop and ask me.

## Step 3: Write the plan, then wait

Create `data/synthetic/PLAN.yaml` containing:
- the 56-person roster with `login`, `name`, `team`, `role`, `group`, `start_date`, `end_date`, `review_strength` by module, `reviews_per_week`, and `out_of_office` where applicable
- the 14 modules and the CODEOWNERS rules (25+, with nested overrides, two stale team handles, two unowned modules)
- the planted facts from the main spec (section 4) mapped to Q1 to Q20
- the planted scenarios R1 to R8 mapped to specific people and PR numbers
- the tier you expect to reach and the counts for PRs, issues, comments, and docs

Show me `PLAN.yaml`. **Do not generate the dataset until I approve it.**

## Step 4: Generate in stages, validating after each

After approval, generate in this order. Commit after each stage with a message naming it (`stage 1: people and CODEOWNERS`, and so on).

1. **People and teams:** `people.json`, `teams.json`, CODEOWNERS. Run the self-review and concentration checks on the roster. Validate.
2. **Modules and files:** the file tree (about 350 files). Source files must parse (`python -m py_compile`); configs must load. Validate.
3. **Pull requests in date order:** 600 to 800 PRs across 12 months, reviews on at least 85% of merged PRs, reviewers chosen from `review_strength` and `reviews_per_week`, never the author, never anyone on leave or after their `end_date`, bots on about 30% of dependency and security PRs. Write `pulls/{number}.json` and `events.jsonl`. Validate.
4. **Issues and comments:** 350 issues, 40% linked by `Fixes #N` or `Closes #N` to real PRs; 3,000+ review comments; 1,000+ issue comments. Validate.
5. **Documents:** 45 markdown files (12 ADRs, 10 runbooks, 14 module READMEs, 9 guides) with explicit `#123` references and file paths. Validate.
6. **Planted facts and scenarios:** write the Q1 to Q20 and R1 to R8 plants into the data, then the 20+ distractors. Update `ground_truth.json`. Validate.
7. **Change script:** `scripts/apply_changes.py` with steps 1 to 3. Test that each step is idempotent and writes `changes/step_N.json`.
8. **Ingestion test:** `tests/test_synthetic_fixtures.py` must show that the existing ingestion code reads these fixtures through the same code path as the live GitHub API.
9. **Validation report:** run `scripts/validate_dataset.py` and paste its real output into `VALIDATION_REPORT.md`, including the people table from the addendum section 7.

## Step 5: Verify before saying done

- Re-run `generate_synthetic.py` with the same seed. The SHA-256 in `MANIFEST.json` must match. If it doesn't, the generator is not deterministic: fix it before continuing.
- Every number in `VALIDATION_REPORT.md` must come from a command you ran in this session.
- Do not write "all checks pass" unless the script printed that.
- If a count is short, report the tier reached. Do not pad with random noise.

## Step 6: Report back

Reply with:
1. The tier reached and each entity count against its target
2. Any spec items you could not do, and why
3. The SHA-256 of the dataset
4. The R1 to R8 and Q1 to Q20 coverage (each present or missing)
5. The AI tool and model you used, for the AI disclosure

Then update `PROGRESS.md` with timestamps and the real command output.

## Rules for the whole task

- Never print, log, or commit tokens or keys. Read them from `.env`.
- Never create GitHub accounts. Never copy text from real repositories.
- Use fictional names, `example.com` emails, and clearly fake tokens (`FAKE_TOKEN_DO_NOT_USE`).
- Keep the generator simple enough that I can explain every part of it.
- Stop and ask me rather than guessing at anything the two specs leave open.
