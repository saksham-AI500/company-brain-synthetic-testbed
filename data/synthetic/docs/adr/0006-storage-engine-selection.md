# ADR 0006: Secondary Storage Engine Selection

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
