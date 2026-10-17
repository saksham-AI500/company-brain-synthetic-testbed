# ADR 0009: Circuit Breakers and Adaptive Retry Policy

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
