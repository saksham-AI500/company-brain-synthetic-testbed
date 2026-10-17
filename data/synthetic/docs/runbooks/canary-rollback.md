# Runbook: Automated Canary Rollback

- **Service:** Kubernetes Deployer
- **Severity:** Sev-1
- **Related Issues:** #260, #520
- **Related PRs:** #520

## Overview
Emergency rollback when canary pod error rate exceeds 1%.
Execute rollback command via [infra/deploy/rollback.py](../../infra/deploy/rollback.py).
