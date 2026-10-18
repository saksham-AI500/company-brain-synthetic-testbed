# ADR 0008: MFA Mandate

- **Status:** Accepted
- **Deciders:** Ananya Rao, Zoe Kravitz, Priya Sharma
- **Date:** 2026-03-01
- **Related Issues:** #160, #175
- **Related PRs:** #240, #255

## Context
Enhancing identity security and access control policies in [auth/mfa/totp.py](../../auth/mfa/totp.py).

## Decision
Mandate Multi-Factor Authentication (MFA) via RFC 6238 TOTP standards for all production console and administrative operations.

## Consequences
- Requires TOTP registration during onboarding.
- Integrates with Google Authenticator and enterprise password managers.
