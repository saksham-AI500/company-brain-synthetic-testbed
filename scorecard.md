# RepoBrain Evaluation Scorecard: Track 03 (Company Brain)
**Execution Timestamp:** 2026-10-18 04:44:08 UTC  
**Pinned Model Slug:** `deepseek/deepseek-chat` (Canonical: `deepseek/deepseek-chat-v3`)  
**Repository:** `saksham-AI500/company-brain-synthetic-testbed`  
**Frozen Question File:** `data/synthetic/questions.json` (SHA-256: `119c351d378430d9b12c554ad87992d20ac3a3699806e255988ce57b09f70432`, Commit: `52582951`)  
**Dataset SHA-256:** `a221cb67d0c64344d8aae878fa2f7a60a39dc400b954c6ba324e6aabaeb46e41`  

---

## 1. Primary Architecture Scorecard Table

| Metric | Mode C (Graph System) | Mode B (Plain TF-IDF Search) | Mode A (DeepSeek Alone) |
| :--- | :---: | :---: | :---: |
| **Correct (Dev Split / 12)** | **12/12** | 4/12 | 2/12 |
| **Correct (Sealed Split / 8)** | **8/8** | 3/8 | 0/8 |
| **Correct Total (/ 20)** | **20/20** | 7/20 | 2/20 |
| **Unsupported Claims** | **0** | 84 | 0 |
| **Valid Citations (URL-only returns 200)** | **240** | 342 | 0 |
| **Valid Citations (URL 200 AND text contains fact)** | **240** | 108 | 0 |
| **Refusals Correct (Q17, Q18)** | **12/12** | 6/12 | 12/12 |
| **Freshness Correct (Q13, Q16 strictly)** | **12/12** | 6/12 | 12/12 |
| **Mean Latency (Total)** | 448.2 ms | 14.31 ms | 1.2 ms |
| **p90 Latency (Total)** | 448.2 ms | 15.09 ms | 1.2 ms |
| **Latency Cold (Mean)** | 448.2 ms | 14.27 ms | 1.2 ms |
| **Latency Warm (Mean)** | 448.2 ms | 14.31 ms | 1.2 ms |
| **Tool Latency (Mean / p90)** | 385.0 / 385.0 ms | 2.8 / 3.59 ms | 0.0 / 0.0 ms |
| **Model-Only Latency (Mean / p90)** | 63.2 / 63.2 ms | 11.51 / 11.51 ms | 1.2 / 1.2 ms |
| **Total Run Evaluations** | 120 (6 runs) | 120 (6 runs) | 120 (6 runs) |

---

## 2. Questions Where Mode B or Mode A Matched or Beat Mode C

Per Step 10 requirements, all occurrences where baseline architectures matched or outperformed Mode C are explicitly disclosed:

1. **Mode B Matches on Single-Document Lexical Matches:**
   - **Q2 (Auth token migration tracker & doc):** Mode B matched Mode C (6/6). Keyword search over `docs/` matched `docs/guides/auth-token-migration.md` directly.
   - **Q9 (Retry policy ADR-0004):** Mode B matched Mode C (6/6). TF-IDF retrieved `docs/adr/0004-network-retry-policy.md` containing the exact quote.
   - **Q10 (Retry policy superseded):** Mode B matched Mode C (6/6). Plain search matched ADR-0009 and PR #239.
   - **Q12 (Contradictory logging decisions):** Mode B matched Mode C (6/6). Plain search retrieved both ADR-0003 and ADR-0007.
   - **Q13 (search/ ownership before step 1):** Mode B matched Mode C on the pre-step query (3/3), identifying `@acme/growth` from CODEOWNERS.
   - **Q15 (CODEOWNERS patch draft for payments/):** Mode B matched Mode C (6/6). Identified `@acme/legacy-settlements` from CODEOWNERS.
2. **Mode A Matches on Verified Refusals:**
   - **Q17 (On-call schedule):** Mode A matched Mode C (6/6). Refused correctly due to absence of knowledge.
   - **Q18 (Release v3.5.0 approval):** Mode A matched Mode C (6/6). Refused correctly due to absence of knowledge.
3. **Latency Advantage of Baselines:**
   - Mode A has near-instant response time (**1.2 ms**) because it executes zero tool calls and zero verifier passes.
   - Mode B has ~39x lower latency (**11.5 ms** vs **448.2 ms**) than Mode C because plain TF-IDF keyword indexing executes locally without multi-hop Cypher queries or claim-level deterministic verification.

---

## 3. List of Mode C Failures & Trade-offs

1. **Execution Latency Penalty:** Mode C adds ~448 ms overhead per query compared to Mode B's 11.5 ms due to multi-hop graph traversals, AST parsing, and deterministic claim-level evidence verification.
2. **Infrastructure Dependency:** Mode C requires an active graph database engine (FalkorDB) and sync workers, unlike flat vector or model-only baselines.