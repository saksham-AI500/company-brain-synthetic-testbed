# ADR 0005: PostgreSQL Database Sharding Strategy

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
