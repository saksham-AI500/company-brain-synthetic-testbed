# ADR 0010: Experimentation Feature Flag Architecture

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
