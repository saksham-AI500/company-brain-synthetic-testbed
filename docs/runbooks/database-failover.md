# Runbook: PostgreSQL Database Primary Failover

- **Service:** PostgreSQL Cluster
- **Severity:** Sev-1
- **Related Issues:** #55, #110
- **Related PRs:** #112

## Immediate Actions
1. Confirm primary database failure using [infra/observability/healthcheck.py](../../infra/deploy/healthcheck.py).
2. Promote standby replica to primary using Patroni orchestrator.
3. Update connection string in [infra/deploy/deploy.yaml](../../infra/deploy/deploy.yaml).
