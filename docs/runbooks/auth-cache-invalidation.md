# Runbook: Identity Token Cache Invalidation

- **Service:** Auth & Session Cache
- **Severity:** Sev-2
- **Related Issues:** #78, #120
- **Related PRs:** #220, #420

## Overview
Flushing compromised or stale JWT verification caches in Redis.
Refer to [auth/revocation_list.py](../../auth/revocation_list.py) and PR #420 token verification cache optimization.
