# Runbook: Payment Pipeline Recovery and Settlement

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
