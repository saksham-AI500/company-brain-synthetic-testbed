# Runbook: SEV-1 Incident Response Protocol

- **Service:** Platform Engineering
- **Severity:** Sev-1
- **Related Issues:** #42, #180
- **Related PRs:** #145

## Overview
Standard escalation policy for customer-impacting platform outages.
Trigger PagerDuty incident in [infra/observability/pagerduty.py](../../infra/observability/pagerduty.py).
