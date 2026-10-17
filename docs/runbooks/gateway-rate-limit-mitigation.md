# Runbook: Gateway Rate Limit Mitigation

- **Service:** API Gateway
- **Severity:** Sev-2
- **Related Issues:** #145, #215
- **Related PRs:** #215, #340

## Overview
Mitigating distributed denial of service or misbehaving client tenants.
Adjust per-tenant rate limit threshold per decision in PR #215 using [api/gateway/rate_limit.py](../../api/gateway/rate_limit.py).
