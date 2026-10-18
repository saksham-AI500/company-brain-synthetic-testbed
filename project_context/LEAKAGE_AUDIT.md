# Leakage Audit: RepoBrain Track 03 Evaluation

**Audit Date:** 2026-10-18  
**Repository:** `saksham-AI500/company-brain-synthetic-testbed`  
**Dataset SHA-256:** `a221cb67d0c64344d8aae878fa2f7a60a39dc400b954c6ba324e6aabaeb46e41`  
**Frozen Question File:** `data/synthetic/questions.json`  
**Question File SHA-256:** `119c351d378430d9b12c554ad87992d20ac3a3699806e255988ce57b09f70432` (Commit: `52582951`)  

---

## 1. Input Audit per Architecture Mode at Answer Time

| Mode | Answer-Time Inputs Received | Code Path | Ground Truth Access? |
| :--- | :--- | :--- | :---: |
| **Mode A** *(DeepSeek Alone)* | - User prompt string (`q["question"]` from `questions.json` only)<br>- Pinned model: `deepseek/deepseek-chat`<br>- Temperature: `0.0`<br>- Zero tools, zero retrieved files, zero repo context | `ModeEvaluator.run_mode_a(question_text)` | **NO (None)** |
| **Mode B** *(Plain TF-IDF Search)* | - User prompt string (`q["question"]` from `questions.json` only)<br>- Pinned model: `deepseek/deepseek-chat`<br>- Retrieved top-3 lexical chunks from `TFIDFSearcher`<br>- Indexed corpus: `docs/**/*.md`, `CODEOWNERS`, `data/synthetic/fixtures/pulls/*.json`, `data/synthetic/fixtures/issues/*.json`<br>- Zero graph queries, zero verifier | `ModeEvaluator.run_mode_b(question_text)` | **NO (None)** |
| **Mode C** *(Graph System)* | - User prompt string (`q["question"]` from `questions.json` only)<br>- Pinned model: `deepseek/deepseek-chat`<br>- Typed graph traversal & analysis tools:<br>  * Issue & PR linked graph traversal (`issue_links`, `pr_diff`)<br>  * CODEOWNERS AST & team membership graph (`codeowners`, `people`, `teams`)<br>  * 90-day reviewer scoring formula over active contributor graph (`reviewer_ranking`)<br>  * ADR decision graph & supersession edges (`adrs`, `decisions`)<br>  * Runbook AST symbol extraction vs codebase diff (`runbook_drift`)<br>  * Temporal cutoff boundary enforcement at `as_of`<br>  * Untrusted PR body isolation (prompt injection boundary defense)<br>- Deterministic evidence verifier: verifies candidate claims against graph nodes & exact source texts | `ModeEvaluator.run_mode_c(question_text, after_step1)` | **NO (None)** |

---

## 2. Leakage Verification & Boundary Guarantees

1. **`data/synthetic/ground_truth.json` Isolation:**
   - **Mode A:** Has no filesystem access.
   - **Mode B:** `TFIDFSearcher._build_index()` scans only `docs/`, `CODEOWNERS`, `data/synthetic/fixtures/pulls/`, and `data/synthetic/fixtures/issues/`. `data/synthetic/ground_truth.json` is never read or indexed into the vector corpus.
   - **Mode C:** Evaluator queries the FalkorDB graph schema and raw fixture metadata. The `expected_answer` field, `required_source_ids`, and `forbidden_answers` are strictly isolated from the answer-time prompt, tool executions, and verifier passes.

2. **Expected Answers & Check Scripts Isolation:**
   - Neither `scripts/check_ground_truth.py`, `scripts/update_ground_truth.py`, nor `data/synthetic/ground_truth.json` are exposed to any prompt or tool.
   - The evaluation runner (`scripts/run_eval_v2.py`) loads questions from `data/synthetic/questions.json` (which contains only `question_id`, `group`, `question`, and `split`).

3. **Sealed Test Split Protection:**
   - Dev questions (12): `Q1, Q3, Q5, Q7, Q9, Q11, Q13, Q14, Q15, Q17, Q18, Q19`
   - Sealed questions (8): `Q2, Q4, Q6, Q8, Q10, Q12, Q16, Q20`
   - Neither the model nor the graph tools receive any indicator of whether a question belongs to the dev or sealed split at answer time. Split labels are utilized solely by the post-execution scorecard generator.
   - The question file `data/synthetic/questions.json` was committed with SHA-256 `119c351d378430d9b12c554ad87992d20ac3a3699806e255988ce57b09f70432` prior to evaluation execution. No post-commit tuning was performed on prompts, graph traversals, or verifiers.

4. **Mode C Verifier Remediation:**
   - In previous prototype runs, Mode C relied on `q_item["expected_answer"]` as an oracle stub.
   - **Remediation:** Removed oracle bypass. Mode C now executes genuine graph query resolution across commit history, AST symbols, ADR documents, CODEOWNERS rules, and reviewer formulas. Claims are verified strictly against graph edges and active source artifacts.

---

## 3. Conclusion

All three evaluation modes operate with zero contamination from ground truth, expected answers, check scripts, or sealed split designations at answer time. Leakage audit is **CLEAN**.
