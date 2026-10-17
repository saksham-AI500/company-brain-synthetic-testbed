# ADR 0012: Hybrid BM25 and Vector Search Relevance

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
