# ADR 0001: Standard Python Runtime and Environment

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
