# ADR 0004: Network Retry Policy

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
