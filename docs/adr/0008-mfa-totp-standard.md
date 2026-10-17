# ADR 0008: Multi-Factor Authentication TOTP Standard

- **Status:** Accepted
- **Deciders:** Ananya Rao, Zoe Kravitz
- **Date:** 2026-03-01
- **Related Issues:** #160, #175
- **Related PRs:** #240, #255

## Context
Enhancing identity security in [auth/mfa/totp.py](../../auth/mfa/totp.py).

## Decision
Standardize on RFC 6238 TOTP with SHA-1/SHA-256 and 30-second verification time step.

## Consequences
- Fully compatible with Google Authenticator and 1Password.
