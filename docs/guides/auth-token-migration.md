# Architecture Guide: Auth Token v2 Migration

- **Tracking Issue:** #78
- **Author:** Ananya Rao
- **Module:** [auth/](../../auth/tokens.py)

## Overview
Migration from symmetric HMAC token verification to asymmetric RSA/ECDSA key pairs.
Covers transition of [auth/session.py](../../auth/session.py) and integration with [api/gateway](../../api/gateway/router.py).
Track progress in open issue #78.
