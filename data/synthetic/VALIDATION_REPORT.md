# Validation Report: Acme Platform Inc. Synthetic Dataset

**Status:** `ALL CHECKS PASSED: DATASET COMPLIANT WITH SPECIFICATION`  
**Tier Reached:** `Tier 1: Full Scale`  
**Dataset SHA-256:** `a221cb67d0c64344d8aae878fa2f7a60a39dc400b954c6ba324e6aabaeb46e41`  
**Deterministic Seed:** `20260930`  
**Timestamp:** `2026-10-18 04:55:59 UTC`

---

## 1. Scale Targets and Actual Counts

| Entity | Target | Actual Count | Status |
|---|---|---|---|
| **Time Span** | 12 months | 12 months (2025-10-01 to 2026-09-30) | **PASS** |
| **People (Total)** | 56 | 56 | **PASS** |
| **Current Employees** | 44 | 44 | **PASS** |
| **Former Employees** | 5 | 5 | **PASS** |
| **Contractors** | 3 | 3 | **PASS** |
| **Bots** | 4 | 4 | **PASS** |
| **Teams** | 4 | 4 | **PASS** |
| **Modules** | 14 | 14 | **PASS** |
| **Files in Repository** | ~350 files | 342 files | **PASS** |
| **Pull Requests** | 600 to 800 | 720 | **PASS** |
| **Commits** | >= 2,000 | 2578 | **PASS** |
| **Issues** | 350 | 350 | **PASS** |
| **Review Comments** | >= 3,000 | 3823 | **PASS** |
| **Issue Comments** | >= 1,000 | 1434 | **PASS** |
| **Documents (MD)** | 45 | 45 | **PASS** |
| **Explicit Decisions** | 25 | 25 | **PASS** |
| **Planted Questions (Q1-Q20)** | 20 | 20 | **PASS** |
| **Planted Scenarios (R1-R8)** | 8 | 8 | **PASS** |
| **Distractor Facts** | >= 20 | 22 | **PASS** |

---

## 2. Validation Checks Summary

1. **Check 1 (Scale Targets):** PASS - All entity counts meet or exceed Tier 1 targets.
2. **Check 2 (Timeline and Chronology):** PASS - All events within 12-month window; reviews strictly after PR creation.
3. **Check 3 (Issue Linkage):** PASS - 140 PRs link to existing issues via `Fixes #N` or `Closes #N`.
4. **Check 4 (File Paths in Tree):** PASS - Every file path exists in codebase tree.
5. **Check 5 (Planted Facts Q1-Q20):** PASS - All 20 planted facts verified present in raw fixtures.
6. **Check 6 (Distractor Facts):** PASS - 22 distractors present and marked.
7. **Check 7 (Deterministic Hash):** PASS - SHA-256 `a221cb67d0c64344d8aae878fa2f7a60a39dc400b954c6ba324e6aabaeb46e41` verified reproducible.
8. **Check 8 (Privacy & Fake Tokens):** PASS - Zero emails outside `@example.com`; all secrets marked `FAKE_TOKEN_DO_NOT_USE`.
9. **Check 9 (Code Compilation & Configs):** PASS - All Python files compile with `py_compile`; all YAML/JSON configs parse.
10. **Check 10 (Bot Review Distribution):** PASS - Bots participate in automated dependency and security reviews.

### Addendum Checks:
- **Addendum Check 1 (People Split):** PASS - 44 current, 5 former, 3 contractors, 4 bots (total 56).
- **Addendum Check 2 (Former Employee Exit):** PASS - Strict zero commits, reviews, or comments after `end_date`.
- **Addendum Check 3 (Self-Review Prohibition):** PASS - Zero self-reviews detected across all 720 PRs.
- **Addendum Check 4 (Review Concentration Cap):** PASS - Top human reviewer (devon-reed) accounts for 7.14% of reviews (<= 25% limit).
- **Addendum Check 5 (Scenarios R1-R8):** PASS - Scenarios R1 through R8 present and verified in ground truth.
- **Addendum Check 6 (Exact Mathematical Tie R2):** PASS - Caleb Rivers and Clara Oswald have identical scores (0.835) to 3 decimal places on 2026-03-20.

---

## 3. 56-Person Detailed Roster Table

| Login | Team | Role | Group | Reviews (90d) | Reviews (12m) | Modules Reviewed |
|---|---|---|---|---|---|---|
| `caleb-rivers` | @acme/platform | Staff Platform Engineer | current | 19 | 62 | api/gateway/, auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `clara-oswald` | @acme/platform | Senior Infrastructure Engineer | current | 17 | 62 | api/gateway/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, infra/observability/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `devon-reed` | @acme/platform | Principal Systems Architect | current | 20 | 79 | api/gateway/, auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, search/, search/indexer/, shared/utils/ |
| `liam-chen` | @acme/platform | Site Reliability Engineer | current | 2 | 22 | api/gateway/, auth/, auth/mfa/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `maya-lin` | @acme/platform | Backend Engineer | current | 6 | 15 | api/gateway/, growth/experiments/, infra/deploy/, notifications/, search/, search/indexer/, shared/utils/ |
| `sophia-rossi` | @acme/platform | Observability Engineer | current | 5 | 17 | auth/, auth/mfa/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `mateo-silva` | @acme/platform | Cloud Infrastructure Engineer | current | 3 | 11 | auth/, auth/mfa/, growth/referrals/, infra/deploy/, notifications/, payments/, search/, search/indexer/, shared/utils/ |
| `aiden-cross` | @acme/platform | DevOps Engineer | current | 5 | 16 | api/gateway/, growth/experiments/, infra/deploy/, infra/observability/, notifications/, search/, search/indexer/ |
| `olivia-taylor` | @acme/platform | API Platform Engineer | current | 4 | 11 | api/gateway/, auth/, growth/experiments/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `zane-malik` | @acme/platform | Junior Systems Engineer | current | 6 | 9 | auth/, auth/mfa/, billing/, growth/experiments/, infra/deploy/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `hannah-schmidt` | @acme/platform | Infrastructure Security Engineer | current | 5 | 15 | api/gateway/, auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/deploy/, notifications/, search/, shared/utils/ |
| `kevin-malone` | @acme/platform | Tooling Engineer | current | 1 | 7 | api/gateway/, growth/experiments/, notifications/, payments/, search/, search/indexer/, shared/utils/ |
| `jordan-hayes` | @acme/platform | Senior Cloud Architect | former | 8 | 27 | api/gateway/, billing/, growth/referrals/, infra/deploy/, infra/observability/, payments/, payments/refunds/ |
| `felix-baum` | @acme/platform | Release Engineering Specialist | current | 4 | 12 | api/gateway/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, notifications/, search/ |
| `priya-sharma` | @acme/payments | Engineering Manager & Tech Lead | current | 14 | 56 | api/gateway/, auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `marcus-vance` | @acme/payments | Staff Payments Engineer | current | 11 | 47 | api/gateway/, auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, infra/observability/, payments/, payments/refunds/, search/, shared/utils/ |
| `nora-al-mansoor` | @acme/payments | Senior Payments Core Engineer | current | 5 | 24 | api/gateway/, auth/, auth/mfa/, billing/, growth/referrals/, infra/observability/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `diego-ramirez` | @acme/payments | Ledger & Settlement Engineer | current | 7 | 20 | api/gateway/, auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `chloe-bennett` | @acme/payments | FinTech Compliance Engineer | current | 2 | 10 | auth/, auth/mfa/, billing/, growth/experiments/, infra/deploy/, infra/observability/, payments/, payments/refunds/, search/, search/indexer/ |
| `raj-kulkarni` | @acme/payments | Payments Integrations Engineer | current | 3 | 10 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `amara-okafor` | @acme/payments | Tax & Invoicing Specialist | current | 1 | 7 | auth/, auth/mfa/, billing/, growth/referrals/, shared/utils/ |
| `tariq-aziz` | @acme/payments | Payments Security Consultant | contractor | 1 | 4 | payments/, payments/refunds/ |
| `lina-kostas` | @acme/payments | Disputes & Chargebacks Developer | current | 2 | 9 | auth/, auth/mfa/, billing/, growth/experiments/, infra/deploy/, payments/, payments/refunds/, search/, search/indexer/ |
| `ethan-hunt` | @acme/payments | Junior Backend Developer | current | 0 | 2 | billing/, growth/referrals/ |
| `leila-farah` | @acme/payments | Payments Reliability Engineer | current | 2 | 8 | api/gateway/, growth/experiments/, growth/referrals/, notifications/, payments/, payments/refunds/, search/ |
| `elena-rostova` | @acme/payments | Former Principal Architect | former | 0 | 38 | auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, infra/observability/, payments/, payments/refunds/, search/, search/indexer/ |
| `lucas-vogel` | @acme/payments | Settlements Developer | former | 0 | 3 | notifications/, payments/, payments/refunds/, search/ |
| `ananya-rao` | @acme/identity | Staff Identity Architect | current | 13 | 41 | api/gateway/, auth/, auth/mfa/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, shared/utils/ |
| `gabriel-santos` | @acme/identity | Senior Security & Auth Engineer | current | 9 | 42 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `zoe-kravitz` | @acme/identity | MFA Protocols Engineer | current | 4 | 18 | auth/, auth/mfa/, growth/referrals/, infra/deploy/, search/, search/indexer/ |
| `owen-murphy` | @acme/identity | OAuth & Token Engineer | current | 1 | 14 | api/gateway/, auth/, auth/mfa/, growth/experiments/, growth/referrals/, payments/, payments/refunds/ |
| `fatima-zahra` | @acme/identity | Directory & IAM Engineer | current | 2 | 7 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/observability/, notifications/, payments/, payments/refunds/, shared/utils/ |
| `kai-nielsen` | @acme/identity | Cryptography & Session Specialist | current | 3 | 15 | auth/, auth/mfa/, growth/referrals/, notifications/, search/, search/indexer/ |
| `isabella-martinez` | @acme/identity | Auth Integration Engineer | current | 1 | 9 | auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, payments/, payments/refunds/, search/, search/indexer/ |
| `hugo-leclerc` | @acme/identity | Security Operations Engineer | current | 1 | 8 | api/gateway/, auth/, auth/mfa/, growth/referrals/, payments/ |
| `tanya-popova` | @acme/identity | Junior Auth Engineer | current | 1 | 6 | growth/experiments/, growth/referrals/, notifications/, search/, search/indexer/, shared/utils/ |
| `ben-carter` | @acme/identity | Compliance & Privacy Engineer | current | 2 | 7 | api/gateway/, auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, infra/deploy/, payments/, payments/refunds/ |
| `samir-patel` | @acme/identity | IAM Specialist | former | 0 | 11 | auth/, auth/mfa/, growth/referrals/, infra/observability/, notifications/ |
| `arjun-mehta` | @acme/growth | Principal Growth Architect | current | 17 | 73 | billing/, growth/experiments/, growth/referrals/, infra/deploy/, notifications/, search/, search/indexer/, shared/utils/ |
| `emma-lindqvist` | @acme/growth | Staff Data & Search Engineer | current | 11 | 53 | api/gateway/, auth/, auth/mfa/, billing/, growth/experiments/, growth/referrals/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `lucia-moretti` | @acme/growth | Experimentation Engine Lead | current | 5 | 14 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, notifications/, payments/ |
| `noah-kim` | @acme/growth | Notification Pipeline Engineer | current | 5 | 22 | notifications/, search/, search/indexer/, shared/utils/ |
| `yuki-tanaka` | @acme/growth | Search Relevance Developer | current | 7 | 21 | api/gateway/, auth/, auth/mfa/, growth/experiments/, notifications/, search/, search/indexer/ |
| `carlos-mendez` | @acme/growth | Referrals & Viral Loop Engineer | current | 6 | 20 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/deploy/, notifications/, search/, search/indexer/ |
| `ingrid-berg` | @acme/growth | Push & Email Delivery Engineer | current | 6 | 16 | auth/, auth/mfa/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `hassan-el-sayed` | @acme/growth | Growth Analytics Developer | current | 2 | 11 | api/gateway/, growth/experiments/, growth/referrals/, infra/observability/, search/, search/indexer/, shared/utils/ |
| `mila-jovanovic` | @acme/growth | Search Crawler Engineer | current | 7 | 13 | api/gateway/, auth/, auth/mfa/, growth/referrals/, notifications/, payments/, payments/refunds/, search/, search/indexer/ |
| `leo-dupont` | @acme/growth | Junior Growth Engineer | current | 0 | 10 | growth/experiments/, growth/referrals/, infra/observability/, payments/, payments/refunds/, search/, search/indexer/ |
| `rachel-green-fictional` | @acme/growth | A/B Testing Specialist | current | 3 | 12 | auth/, auth/mfa/, growth/experiments/, growth/referrals/, infra/observability/, notifications/, search/, search/indexer/, shared/utils/ |
| `maya-zheng` | @acme/growth | Search Indexer Engineer | former | 0 | 16 | auth/, auth/mfa/, billing/, growth/referrals/, notifications/, search/, search/indexer/ |
| `fiona-gallagher` | None (External) | External CI/CD Consultant | contractor | 2 | 5 | infra/deploy/ |
| `dmitri-volkov` | None (External) | External Search Optimization Specialist | contractor | 2 | 8 | search/, search/indexer/ |
| `ci-review-bot[bot]` | None (External) | Automated Review Bot | bot | 2 | 11 | api/gateway/, auth/, auth/mfa/, growth/experiments/, infra/deploy/, payments/, payments/refunds/, shared/utils/ |
| `dependency-bot[bot]` | None (External) | Automated Dependency Scanner | bot | 2 | 11 | auth/, auth/mfa/, infra/deploy/, infra/observability/, notifications/, payments/, payments/refunds/, search/, search/indexer/, shared/utils/ |
| `security-scan[bot]` | None (External) | Automated Security Audit Bot | bot | 1 | 4 | growth/experiments/, infra/observability/, search/, search/indexer/ |
| `docs-lint[bot]` | None (External) | Automated Docs Validator | bot | 0 | 5 | auth/, auth/mfa/, billing/, infra/deploy/, infra/observability/ |
