# Runbook: Dead Letter Queue Recovery

- **Service:** RabbitMQ Worker Pipeline
- **Severity:** Sev-3
- **Related Issues:** #310, #405
- **Related PRs:** #450

## Overview
Reprocessing failed notification jobs from [notifications/dead_letter.py](../../search/indexer/dead_letter.py).
