# ADR 0007: OpenTelemetry OTLP gRPC Log Streaming

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
