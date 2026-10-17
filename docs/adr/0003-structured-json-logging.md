# ADR 0003: Structured JSON Logging to Standard Output

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
