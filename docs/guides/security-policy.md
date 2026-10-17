# Security and Secrets Policy

- Never commit real credentials or tokens.
- Mark all test fixture tokens as `FAKE_TOKEN_DO_NOT_USE`.
- Encrypted secrets managed via Vault loader in [infra/deploy/secrets_loader.py](../../infra/deploy/secrets_loader.py).
