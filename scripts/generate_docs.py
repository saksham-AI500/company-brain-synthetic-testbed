"""
Deterministic Documentation Generator for Acme Platform Inc.
Generates 45 markdown documents (12 ADRs, 10 runbooks, 14 module READMEs, 9 guides).
All docs contain explicit #123 issue/PR references and file path links.
"""
import os
import shutil

def create_doc(rel_path, content):
    for base in ["docs", os.path.join("data", "synthetic", "docs")]:
        full_p = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_p), exist_ok=True)
        with open(full_p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def run():
    print("Generating 45 markdown documents...")
    docs_created = []

    # ==========================================
    # 1. 12 Architecture Decision Records (ADRs)
    # ==========================================
    adrs = {
        "0001-python-runtime.md": """# ADR 0001: Standard Python Runtime and Environment

- **Status:** Accepted (Partially updated in #50)
- **Deciders:** Caleb Rivers, Priya Sharma, Devon Reed
- **Date:** 2025-10-05
- **Related Issues:** #5, #10
- **Related PRs:** #15, #50

## Context
Acme Platform requires a unified Python runtime across all microservices and worker nodes.

## Decision
We adopt Python 3.11 as the standard production runtime.
All packaging is standardized via [pyproject.toml](../../pyproject.toml).

## Consequences
- Requires updating base Docker images across all services.
- Distractor note: Earlier drafts referenced Python 3.9 before PR #50 updated runtime dependencies.
""",

        "0002-microservices-communication.md": """# ADR 0002: Service Communication Protocols

- **Status:** Accepted
- **Deciders:** Devon Reed, Marcus Vance, Ananya Rao
- **Date:** 2025-10-12
- **Related Issues:** #18, #22
- **Related PRs:** #28, #35

## Context
High volume inter-service RPC communication between [api/gateway](../../api/gateway/router.py) and backend modules.

## Decision
We use HTTP/2 with JSON payloads for external client ingress, and gRPC with Protobuf for high-throughput internal microservice calls.

## Consequences
- High performance RPC communication.
- Rate limiting handled at ingress gateway per #215.
""",

        "0003-structured-json-logging.md": """# ADR 0003: Structured JSON Logging to Standard Output

- **Status:** Accepted (Contradicted by ADR-0007)
- **Deciders:** Liam Chen
- **Date:** 2025-10-20
- **Related Issues:** #12, #30
- **Related PRs:** #40, #65

## Context
Uniform log parsing is necessary for container log aggregation in Kubernetes clusters.

## Decision
All services must log structured JSON objects strictly to standard output (`stdout`).
Log lines must adhere to the schema implemented in [infra/observability/logger.py](../../infra/observability/logger.py).

## Consequences
- Native integration with Kubernetes log shippers (Fluentbit).
- Note: This decision was later contradicted by ADR-0007 (authored by Sophia Rossi on 2026-02-14) which mandates direct OTLP gRPC streaming.
""",

        "0004-network-retry-policy.md": """# ADR 0004: Network Retry Policy

- **Status:** Superseded by ADR-0009
- **Deciders:** Devon Reed, Elena Rostova
- **Date:** 2025-11-15
- **Related Issues:** #25, #45
- **Related PRs:** #75, #340

## Context
Network jitter and transient socket timeouts between internal services cause occasional request drops.

## Decision
Retry policy: exponential backoff with jitter, max 5 attempts.
Base retry interval is set to 100ms with a backoff multiplier of 2.0.

## Consequences
- Mitigates momentary network blips.
- Superseded on 2026-04-10 by ADR-0009 and PR #340 due to retry storms under heavy degradation.
""",

        "0005-database-sharding.md": """# ADR 0005: PostgreSQL Database Sharding Strategy

- **Status:** Accepted
- **Deciders:** Clara Oswald, Marcus Vance
- **Date:** 2025-12-05
- **Related Issues:** #55, #62
- **Related PRs:** #90, #112

## Context
Scaling the relational ledger in [payments/ledger.py](../../payments/ledger.py) past 10 million transactions.

## Decision
Shard transaction records across 8 database shards partitioned on tenant UUID.

## Consequences
- Requires distributed transactions and reconciliation scripts in [payments/refunds/reconciliation.py](../../payments/refunds/reconciliation.py).
""",

        "0006-storage-engine-selection.md": """# ADR 0006: Secondary Storage Engine Selection

- **Status:** Accepted
- **Deciders:** Arjun Mehta, Emma Lindqvist
- **Date:** 2026-01-10
- **Related Issues:** #80, #88
- **Related PRs:** #135

## Context
Evaluation of document database for search index crawler metadata.

## Decision
We select PostgreSQL JSONB and Redis.

## Alternatives Considered
- MongoDB: Considered for document caching, but explicitly rejected due to operational overhead and licensing constraints.
""",

        "0007-opentelemetry-grpc-logging.md": """# ADR 0007: OpenTelemetry OTLP gRPC Log Streaming

- **Status:** Accepted (Contradicts ADR-0003)
- **Deciders:** Sophia Rossi
- **Date:** 2026-02-14
- **Related Issues:** #130, #142
- **Related PRs:** #280, #315

## Context
High volume stdout logging creates excessive Docker daemon IOPS on Kubernetes cluster worker nodes.

## Decision
All production services must stream logs via OpenTelemetry OTLP over gRPC directly to the observability collector daemon, bypassing stdout.
Implementation in [infra/observability/collector.py](../../infra/observability/collector.py).

## Consequences
- Bypasses stdout and Docker log rotators.
- Directly contradicts the mandate in ADR-0003.
""",

        "0008-mfa-totp-standard.md": """# ADR 0008: Multi-Factor Authentication TOTP Standard

- **Status:** Accepted
- **Deciders:** Ananya Rao, Zoe Kravitz
- **Date:** 2026-03-01
- **Related Issues:** #160, #175
- **Related PRs:** #240, #255

## Context
Enhancing identity security in [auth/mfa/totp.py](../../auth/mfa/totp.py).

## Decision
Standardize on RFC 6238 TOTP with SHA-1/SHA-256 and 30-second verification time step.

## Consequences
- Fully compatible with Google Authenticator and 1Password.
""",

        "0009-circuit-breakers.md": """# ADR 0009: Circuit Breakers and Adaptive Retry Policy

- **Status:** Accepted (Supersedes ADR-0004)
- **Deciders:** Caleb Rivers, Devon Reed
- **Date:** 2026-04-10
- **Related Issues:** #210, #225
- **Related PRs:** #340, #365

## Context
The 5-attempt exponential backoff from ADR-0004 caused thundering herd failures during gateway brownouts.

## Decision
We formally supersede ADR-0004.
The new policy replaces 5-attempt retry with an aggressive circuit breaker and a maximum of 3 attempts with adaptive backoff.
Implemented in PR #340 and [api/gateway/circuit_breaker.py](../../api/gateway/circuit_breaker.py).

## Consequences
- Rapid failure isolation.
- Completely replaces the 5-attempt policy defined in ADR-0004.
""",

        "0010-feature-flag-architecture.md": """# ADR 0010: Experimentation Feature Flag Architecture

- **Status:** Accepted
- **Deciders:** Lucia Moretti, Arjun Mehta
- **Date:** 2026-05-18
- **Related Issues:** #280, #295
- **Related PRs:** #390, #410

## Context
Low latency runtime feature toggles for growth experiments.

## Decision
Use consistent MurmurHash3 bucketing on user UUID in [growth/experiments/variant_allocator.py](../../growth/experiments/variant_allocator.py).

## Consequences
- Deterministic variant assignment without server-side database lookups.
""",

        "0011-event-driven-notifications.md": """# ADR 0011: Asynchronous Event-Driven Notifications

- **Status:** Accepted
- **Deciders:** Noah Kim, Ingrid Berg
- **Date:** 2026-06-22
- **Related Issues:** #315, #330
- **Related PRs:** #480, #505

## Context
Decoupling billing and checkout notifications from user synchronous request loop.

## Decision
Emit domain events to RabbitMQ topic exchange, consumed by [notifications/dispatcher.py](../../notifications/dispatcher.py).

## Consequences
- Sub-millisecond response latency during checkout.
""",

        "0012-search-relevance-scoring.md": """# ADR 0012: Hybrid BM25 and Vector Search Relevance

- **Status:** Accepted
- **Deciders:** Emma Lindqvist, Dmitri Volkov
- **Date:** 2026-07-30
- **Related Issues:** #345, #360
- **Related PRs:** #580, #615

## Context
Upgrading full-text relevance ranking in [search/ranking.py](../../search/ranking.py).

## Decision
Blend BM25 keyword score (60% weight) with dense vector cosine similarity (40% weight).

## Consequences
- Significantly higher recall for semantic and misspelled queries.
"""
    }

    for name, content in adrs.items():
        rel = os.path.join("adr", name)
        create_doc(rel, content)
        docs_created.append(rel)

    # ==========================================
    # 2. 10 Operational Runbooks
    # ==========================================
    runbooks = {
        "payment-pipeline-recovery.md": """# Runbook: Payment Pipeline Recovery and Settlement

- **Service:** Payments & Settlement Core
- **Severity:** Sev-1 / Sev-2
- **Author:** Elena Rostova (Reviewed by Marcus Vance)
- **Last Updated:** 2025-11-20
- **Related Issues:** #42, #145
- **Related PRs:** #145, #230

## Overview
Procedures for clearing stalled payment settlement queues during database failover or gateway timeouts.

## Step 1: Diagnose Stuck Batches
Inspect pending transaction entries in [payments/ledger.py](../../payments/ledger.py).

## Step 2: Batch Reconciliation (STALE PROCEDURE)
Run the automated reconciliation tool:
```bash
python -m payments.refunds.batch --action reconcile_unsettled_batches
```
> **Warning (Outdated Reference):** Note that `reconcile_unsettled_batches()` was completely removed in PR #230. Calling this function will throw an `AttributeError`. Modern recovery uses streaming ledger reconciliation in [payments/refunds/reconciliation.py](../../payments/refunds/reconciliation.py).

## Step 3: Verify Gateway Health
Verify that [payments/gateway.py](../../payments/gateway.py) circuit breaker is healthy.
""",

        "database-failover.md": """# Runbook: PostgreSQL Database Primary Failover

- **Service:** PostgreSQL Cluster
- **Severity:** Sev-1
- **Related Issues:** #55, #110
- **Related PRs:** #112

## Immediate Actions
1. Confirm primary database failure using [infra/observability/healthcheck.py](../../infra/deploy/healthcheck.py).
2. Promote standby replica to primary using Patroni orchestrator.
3. Update connection string in [infra/deploy/deploy.yaml](../../infra/deploy/deploy.yaml).
""",

        "ssl-cert-renewal.md": """# Runbook: TLS/SSL Certificate Automated Renewal

- **Service:** Ingress Edge Gateway
- **Severity:** Sev-3
- **Related Issues:** #68
- **Related PRs:** #95

## Overview
Procedures for Let's Encrypt automated certificate renewals.
Distractor note: dummy testing cert verification script references cert renewals on annual staging cycles.
Refer to [infra/deploy/cert_manager.py](../../infra/deploy/cert_manager.py).
""",

        "auth-cache-invalidation.md": """# Runbook: Identity Token Cache Invalidation

- **Service:** Auth & Session Cache
- **Severity:** Sev-2
- **Related Issues:** #78, #120
- **Related PRs:** #220, #420

## Overview
Flushing compromised or stale JWT verification caches in Redis.
Refer to [auth/revocation_list.py](../../auth/revocation_list.py) and PR #420 token verification cache optimization.
""",

        "gateway-rate-limit-mitigation.md": """# Runbook: Gateway Rate Limit Mitigation

- **Service:** API Gateway
- **Severity:** Sev-2
- **Related Issues:** #145, #215
- **Related PRs:** #215, #340

## Overview
Mitigating distributed denial of service or misbehaving client tenants.
Adjust per-tenant rate limit threshold per decision in PR #215 using [api/gateway/rate_limit.py](../../api/gateway/rate_limit.py).
""",

        "search-reindexing.md": """# Runbook: Elasticsearch & Shard Reindexing

- **Service:** Search Indexer
- **Severity:** Sev-2
- **Related Issues:** #202, #305
- **Related PRs:** #415, #510

## Overview
Rebuilding search inverted index from Postgres WAL logical replication stream.
Trigger pipeline crawl in [search/indexer/pipeline.py](../../search/indexer/pipeline.py).
""",

        "canary-rollback.md": """# Runbook: Automated Canary Rollback

- **Service:** Kubernetes Deployer
- **Severity:** Sev-1
- **Related Issues:** #260, #520
- **Related PRs:** #520

## Overview
Emergency rollback when canary pod error rate exceeds 1%.
Execute rollback command via [infra/deploy/rollback.py](../../infra/deploy/rollback.py).
""",

        "dead-letter-queue-drain.md": """# Runbook: Dead Letter Queue Recovery

- **Service:** RabbitMQ Worker Pipeline
- **Severity:** Sev-3
- **Related Issues:** #310, #405
- **Related PRs:** #450

## Overview
Reprocessing failed notification jobs from [notifications/dead_letter.py](../../search/indexer/dead_letter.py).
""",

        "incident-response-sev1.md": """# Runbook: SEV-1 Incident Response Protocol

- **Service:** Platform Engineering
- **Severity:** Sev-1
- **Related Issues:** #42, #180
- **Related PRs:** #145

## Overview
Standard escalation policy for customer-impacting platform outages.
Trigger PagerDuty incident in [infra/observability/pagerduty.py](../../infra/observability/pagerduty.py).
""",

        "legacy-auth-failover.md": """# Runbook: Legacy Auth Failover [DEPRECATED]

- **Service:** Legacy Authentication (Decommissioned)
- **Status:** DEPRECATED
- **Related Issues:** #15, #78

## Warning
[DEPRECATED] This runbook is obsolete. Do not use.
References decommissioned cluster auth-prod-01 from 2023. Modern authentication runs on [auth/authenticator.py](../../auth/authenticator.py).
"""
    }

    for name, content in runbooks.items():
        rel = os.path.join("runbooks", name)
        create_doc(rel, content)
        docs_created.append(rel)

    # ==========================================
    # 3. 14 Module READMEs
    # ==========================================
    for m in [
        "auth", "auth_mfa", "payments", "payments_refunds", "billing",
        "search", "search_indexer", "notifications", "growth_experiments",
        "growth_referrals", "infra_deploy", "infra_observability",
        "api_gateway", "shared_utils"
    ]:
        m_display = m.replace("_", "/")
        readme_content = f"""# Module: {m_display}

## Description
Core documentation for `{m_display}` subsystem within Acme Platform Inc.

## Architecture
See related ADRs in [docs/adr/](../../docs/adr/0001-python-runtime.md).

## Ownership
Declared ownership configured in [CODEOWNERS](../../CODEOWNERS).

## Key Components
- Core routines and implementation logic
- Integration test coverage in [tests/](../../tests/)
"""
        rel = os.path.join("modules", f"{m}-README.md")
        create_doc(rel, readme_content)
        docs_created.append(rel)

    # ==========================================
    # 4. 9 Guides (Onboarding, Contributing, Architecture)
    # ==========================================
    guides = {
        "onboarding.md": """# Engineering Onboarding Guide

Welcome to Acme Platform Inc.!

## Setup
1. Clone the repository: `git clone https://github.com/saksham-AI500/company-brain-synthetic-testbed.git`
2. Configure `.env` from template: `cp .env.example .env`
3. Join platform chat channel `#ask-platform` for assistance (see Distractor-17).
""",

        "contributing.md": """# Contributing Guidelines

Please review our PR review process and guidelines.
- Every PR must pass `python -m py_compile` and unit tests.
- Reference issues using `Fixes #N` or `Closes #N`.
- Refer to [docs/guides/code-review-standards.md](code-review-standards.md).
""",

        "auth-token-migration.md": """# Architecture Guide: Auth Token v2 Migration

- **Tracking Issue:** #78
- **Author:** Ananya Rao
- **Module:** [auth/](../../auth/tokens.py)

## Overview
Migration from symmetric HMAC token verification to asymmetric RSA/ECDSA key pairs.
Covers transition of [auth/session.py](../../auth/session.py) and integration with [api/gateway](../../api/gateway/router.py).
Track progress in open issue #78.
""",

        "style-guide.md": """# Python Style Guide

We follow PEP 8 with line length 120.
Updated in PR #108 (note: PR #108 is a false link for checkout bug #42).
""",

        "testing-guidelines.md": """# Testing Guidelines

All unit tests reside in [tests/](../../tests/).
Run tests locally with `pytest tests/`.
""",

        "security-policy.md": """# Security and Secrets Policy

- Never commit real credentials or tokens.
- Mark all test fixture tokens as `FAKE_TOKEN_DO_NOT_USE`.
- Encrypted secrets managed via Vault loader in [infra/deploy/secrets_loader.py](../../infra/deploy/secrets_loader.py).
""",

        "code-review-standards.md": """# Peer Code Review Standards

- Every production PR requires peer approval from declared CODEOWNERS.
- Self-reviews are strictly forbidden across all modules.
- Special handling for cross-module changes (e.g. #350).
""",

        "deployment-runbook.md": """# Deployment Operational Guide

Explains Canary rollout sequence managed by [infra/deploy/canary.py](../../infra/deploy/canary.py).
""",

        "api-design-guide.md": """# REST and gRPC API Design Standards

Standards for error reporting (RFC 7807) and tenant rate-limiting defined in [api/gateway/rate_limit.py](../../api/gateway/rate_limit.py).
"""
    }

    for name, content in guides.items():
        rel = os.path.join("guides", name)
        create_doc(rel, content)
        docs_created.append(rel)

    print(f"Total documents created: {len(docs_created)} (Target: 45)")
    assert len(docs_created) == 45, f"Expected 45 documents, got {len(docs_created)}"
    return docs_created

if __name__ == "__main__":
    run()
