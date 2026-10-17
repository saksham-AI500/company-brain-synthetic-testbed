"""
Generate realistic file tree (~350 files) across 14 modules, tests, configs.
All Python files must compile with py_compile. All configs must load.
"""
import os
import sys
import json
import yaml
import py_compile

def create_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_module_files(module_path, module_name, file_specs):
    for filename, code in file_specs.items():
        full_path = os.path.join(module_path, filename)
        create_file(full_path, code)

def build_all_files():
    print("Generating codebase files across 14 modules...")
    generated_files = []

    # 1. Root configs and project files
    root_files = {
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "acme-platform"
version = "1.8.0"
description = "Acme Platform core backend, services, and infrastructure"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Acme Platform Team", email = "engineering@example.com" }]
dependencies = [
    "pydantic>=2.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.22.0",
    "pyyaml>=6.0",
    "cryptography>=41.0.0",
    "httpx>=0.24.0",
    "redis>=4.5.0",
    "opentelemetry-api>=1.20.0",
    "opentelemetry-sdk>=1.20.0"
]
""",
        "setup.py": """from setuptools import setup, find_packages

setup(
    name="acme-platform",
    version="1.8.0",
    packages=find_packages(),
    python_requires=">=3.11",
)
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.2
pyyaml==6.0.1
cryptography==41.0.7
httpx==0.25.2
redis==5.0.1
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
pytest==7.4.3
pytest-asyncio==0.21.1
""",
        ".env.example": """# Environment configuration template
APP_ENV=development
PORT=8080
DATABASE_URL=postgres://acme_user:FAKE_PASSWORD_DO_NOT_USE@localhost:5432/acme_db
REDIS_URL=redis://localhost:6379/0
API_GATEWAY_SECRET=FAKE_TOKEN_DO_NOT_USE_SECRET123
STRIPE_API_KEY=FAKE_TOKEN_DO_NOT_USE_STRIPE_TEST
""",
        ".gitignore": """__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv/
env/
venv/
dist/
build/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
""",
        "Makefile": """.PHONY: test lint run clean

test:
	pytest tests/

lint:
	python -m py_compile **/*.py

run:
	uvicorn api.gateway.router:app --reload --port 8080

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
""",
        "docker-compose.yml": """version: '3.8'
services:
  gateway:
    build: .
    ports:
      - "8080:8080"
    environment:
      - APP_ENV=local
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: acme_user
      POSTGRES_PASSWORD: FAKE_PASSWORD_DO_NOT_USE
      POSTGRES_DB: acme_db
    ports:
      - "5432:5432"
""",
        "Dockerfile": """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "api.gateway.router:app", "--host", "0.0.0.0", "--port", "8080"]
""",
        ".flake8": """[flake8]
max-line-length = 120
exclude = .git,__pycache__,build,dist,.venv
ignore = E203, W503
"""
    }
    for p, c in root_files.items():
        create_file(p, c)
        generated_files.append(p)

    # 2. GitHub Workflows
    workflow_files = {
        ".github/workflows/ci.yml": """name: Continuous Integration
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint and compile
        run: python -m py_compile $(git ls-files '*.py')
      - name: Run tests
        run: pytest tests/
""",
        ".github/workflows/security.yml": """name: Security Scan
on:
  schedule:
    - cron: '0 2 * * *'
  pull_request:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency Review
        uses: actions/dependency-review-action@v3
""",
        ".github/workflows/release.yml": """name: Release Pipeline
on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build wheel
        run: python -m pip install build && python -m build
"""
    }
    for p, c in workflow_files.items():
        create_file(p, c)
        generated_files.append(p)

    # Helper to generate standard python modules with varied functions
    def gen_py_file(mod, name, doc, funcs):
        lines = [f'"""{doc}"""', "from typing import Dict, Any, List, Optional", "import logging", ""]
        lines.append(f"logger = logging.getLogger('{mod}.{name}')")
        lines.append("")
        for fname, ret, body in funcs:
            lines.append(f"def {fname}(*args, **kwargs) -> {ret}:")
            lines.append(f'    """Implementation for {fname}."""')
            lines.append(f"    logger.debug('Executing {fname} with %s', kwargs)")
            for b in body:
                lines.append(f"    {b}")
            lines.append("")
        return "\n".join(lines)

    # 3. auth/ (20 files)
    auth_files = {
        "__init__.py": '"""Authentication root package."""\n__version__ = "1.8.0"\n',
        "config.yaml": "auth:\n  token_expiry_seconds: 3600\n  refresh_expiry_days: 30\n  issuer: acme-platform-auth\n",
        "README.md": "# Auth Module\nCore identity, token verification, and user sessions.\n",
        "authenticator.py": gen_py_file("auth", "authenticator", "Primary authentication handler.", [
            ("authenticate_credentials", "Dict[str, Any]", ["username = kwargs.get('username')", "return {'authenticated': True, 'user_id': 'usr_1001'}"]),
            ("verify_api_key", "bool", ["key = kwargs.get('api_key', '')", "return key.startswith('acme_pk_')"])
        ]),
        "tokens.py": gen_py_file("auth", "tokens", "JWT and session token minting.", [
            ("create_access_token", "str", ["return 'jwt.header.payload.signature'"]),
            ("validate_access_token", "Dict[str, Any]", ["return {'sub': 'usr_1001', 'valid': True}"]),
            ("revoke_token", "bool", ["return True"])
        ]),
        "session.py": gen_py_file("auth", "session", "User session state management across auth and payments.", [
            ("create_session", "str", ["return 'sess_' + str(kwargs.get('user_id', 'anon'))"]),
            ("get_session", "Optional[Dict[str, Any]]", ["return {'session_id': 'sess_1', 'active': True}"]),
            ("terminate_session", "bool", ["return True"])
        ]),
        "password.py": gen_py_file("auth", "password", "Secure password hashing and validation.", [
            ("hash_password", "str", ["return '$argon2id$v=19$m=65536,t=3,p=4$fakehash'"]),
            ("verify_password", "bool", ["return True"])
        ]),
        "jwt_handler.py": gen_py_file("auth", "jwt_handler", "JSON Web Token encoder and decoder.", [
            ("encode_claims", "str", ["return 'header.claims.signed'"]),
            ("decode_claims", "Dict[str, Any]", ["return {'claims': {'aud': 'acme-api'}}"])
        ]),
        "oauth_provider.py": gen_py_file("auth", "oauth_provider", "OAuth 2.0 grant flow provider.", [
            ("authorize_code", "str", ["return 'code_auth_sample_123'"]),
            ("exchange_token", "Dict[str, str]", ["return {'access_token': 'tok_abc', 'token_type': 'Bearer'}"])
        ]),
        "scopes.py": gen_py_file("auth", "scopes", "RBAC scope definition and checks.", [
            ("check_scope", "bool", ["required = kwargs.get('required', 'read')", "return True"]),
            ("list_user_scopes", "List[str]", ["return ['read:all', 'write:orders', 'profile']"])
        ]),
        "permissions.py": gen_py_file("auth", "permissions", "Permission evaluator.", [
            ("has_permission", "bool", ["return True"])
        ]),
        "rate_limit_auth.py": gen_py_file("auth", "rate_limit_auth", "Login rate limit defense.", [
            ("check_login_rate", "bool", ["return True"])
        ]),
        "identity_store.py": gen_py_file("auth", "identity_store", "Identity backend abstraction.", [
            ("get_identity", "Dict[str, Any]", ["return {'id': 'usr_1001', 'status': 'ACTIVE'}"])
        ]),
        "audit_auth.py": gen_py_file("auth", "audit_auth", "Auth security audit logging.", [
            ("record_auth_event", "None", ["logger.info('Audit event recorded: %s', kwargs)"])
        ]),
        "crypto_keys.py": gen_py_file("auth", "crypto_keys", "RSA/ECDSA key loader.", [
            ("get_public_key_pem", "str", ["return '-----BEGIN PUBLIC KEY-----\\nFAKE_KEY\\n-----END PUBLIC KEY-----'"])
        ]),
        "revocation_list.py": gen_py_file("auth", "revocation_list", "Token revocation bloom filter.", [
            ("is_revoked", "bool", ["return False"])
        ]),
        "claims_mapper.py": gen_py_file("auth", "claims_mapper", "Custom token claims mapper.", [
            ("map_tenant_claims", "Dict[str, Any]", ["return {'tenant_id': 'ten_99'}"])
        ]),
        "service_account.py": gen_py_file("auth", "service_account", "Machine to machine service tokens.", [
            ("verify_service_account", "bool", ["return True"])
        ]),
        "middleware.py": gen_py_file("auth", "middleware", "FastAPI authentication middleware.", [
            ("auth_middleware_handler", "Dict[str, Any]", ["return {'status': 200, 'authenticated': True}"])
        ]),
        "exceptions.py": gen_py_file("auth", "exceptions", "Auth specific exceptions.", [
            ("raise_unauthorized", "None", ["raise PermissionError('Unauthorized access attempt')"])
        ])
    }
    for fname, code in auth_files.items():
        p = os.path.join("auth", fname)
        create_file(p, code)
        generated_files.append(p)

    # 4. auth/mfa/ (15 files)
    mfa_files = {
        "__init__.py": '"""MFA subpackage."""\n',
        "README.md": "# MFA Module\nMulti-factor authentication (TOTP, WebAuthn, SMS).\n",
        "mfa_policy.py": gen_py_file("auth.mfa", "mfa_policy", "MFA enforcement policies.", [
            ("is_mfa_required", "bool", ["return True"]),
            ("get_supported_factors", "List[str]", ["return ['totp', 'webauthn', 'backup_code']"])
        ]),
        "totp.py": gen_py_file("auth.mfa", "totp", "Time-based One Time Password implementation.", [
            ("generate_totp_secret", "str", ["return 'JBSWY3DPEHPK3PXP'"]),
            ("verify_totp_code", "bool", ["return len(str(kwargs.get('code', ''))) == 6"])
        ]),
        "sms_gateway.py": gen_py_file("auth.mfa", "sms_gateway", "SMS dispatch for 2FA.", [
            ("send_verification_sms", "str", ["return 'sms_msg_98213'"])
        ]),
        "backup_codes.py": gen_py_file("auth.mfa", "backup_codes", "Emergency backup recovery codes.", [
            ("generate_backup_codes", "List[str]", ["return ['1234-5678', '8765-4321', '9988-7766']"]),
            ("consume_backup_code", "bool", ["return True"])
        ]),
        "webauthn.py": gen_py_file("auth.mfa", "webauthn", "FIDO2 / WebAuthn passkey authentication.", [
            ("initiate_registration", "Dict[str, Any]", ["return {'challenge': 'chal_xyz123'}"]),
            ("verify_assertion", "bool", ["return True"])
        ]),
        "device_fingerprint.py": gen_py_file("auth.mfa", "device_fingerprint", "Trusted device registration.", [
            ("is_device_trusted", "bool", ["return True"])
        ]),
        "step_up.py": gen_py_file("auth.mfa", "step_up", "Step-up authentication for high risk actions.", [
            ("require_step_up", "bool", ["return True"])
        ]),
        "mfa_notifier.py": gen_py_file("auth.mfa", "mfa_notifier", "Notifications for MFA state changes.", [
            ("notify_factor_enrolled", "None", ["logger.info('Factor enrolled: %s', kwargs)"])
        ]),
        "recovery_vault.py": gen_py_file("auth.mfa", "recovery_vault", "Encrypted recovery token store.", [
            ("store_recovery_data", "bool", ["return True"])
        ]),
        "fido_attestation.py": gen_py_file("auth.mfa", "fido_attestation", "Hardware security key attestation.", [
            ("verify_attestation", "bool", ["return True"])
        ]),
        "audit_mfa.py": gen_py_file("auth.mfa", "audit_mfa", "MFA compliance auditor.", [
            ("log_mfa_attempt", "None", ["pass"])
        ]),
        "challenge_store.py": gen_py_file("auth.mfa", "challenge_store", "Transient redis challenge store.", [
            ("put_challenge", "bool", ["return True"]),
            ("get_challenge", "Optional[str]", ["return 'chal_xyz123'"])
        ]),
        "mfa_errors.py": gen_py_file("auth.mfa", "mfa_errors", "MFA error declarations.", [
            ("get_error_details", "Dict[str, str]", ["return {'code': 'MFA_FAILED'}"])
        ])
    }
    for fname, code in mfa_files.items():
        p = os.path.join("auth", "mfa", fname)
        create_file(p, code)
        generated_files.append(p)

    # 5. payments/ (25 files)
    payments_files = {
        "__init__.py": '"""Payments core package."""\n',
        "config.yaml": "payments:\n  default_currency: USD\n  max_retry_attempts: 3\n  connect_timeout_ms: 5000\n",
        "README.md": "# Payments Core\nPayment gateway, checkout pipelines, and settlement ledger.\n",
        "checkout.py": gen_py_file("payments", "checkout", "Checkout order completion and deadlock prevention.", [
            ("process_checkout", "Dict[str, Any]", [
                "# Fix for issue #42: Set DB connection timeout to 5000ms to avoid deadlocks",
                "timeout_ms = kwargs.get('timeout_ms', 5000)",
                "cart_id = kwargs.get('cart_id', 'cart_default')",
                "return {'status': 'COMPLETED', 'cart_id': cart_id, 'transaction_id': 'tx_987654'}"
            ]),
            ("acquire_checkout_lock", "bool", ["return True"]),
            ("validate_cart_items", "bool", ["return True"]),
            ("release_checkout_lock", "None", ["pass"])
        ]),
        "gateway.py": gen_py_file("payments", "gateway", "Payment gateway connector and circuit breaker.", [
            ("dispatch_payment", "Dict[str, Any]", ["return {'gateway_ref': 'gw_tx_001', 'status': 'AUTHORIZED'}"]),
            ("refund_transaction", "Dict[str, Any]", ["return {'refund_id': 'rf_123', 'status': 'PROCESSED'}"])
        ]),
        "processor.py": gen_py_file("payments", "processor", "Payment processing orchestration.", [
            ("process_payment_intent", "Dict[str, Any]", ["return {'intent_id': 'pi_101', 'state': 'CAPTURED'}"])
        ]),
        "ledger.py": gen_py_file("payments", "ledger", "Double-entry accounting ledger.", [
            ("record_entry", "str", ["return 'entry_ledger_7701'"]),
            ("get_account_balance", "float", ["return 15000.50"])
        ]),
        "transactions.py": gen_py_file("payments", "transactions", "Transaction query service.", [
            ("get_transaction_by_id", "Dict[str, Any]", ["return {'id': 'tx_987654', 'amount': 99.99}"])
        ]),
        "stripe_client.py": gen_py_file("payments", "stripe_client", "Stripe payment network adapter.", [
            ("create_charge", "Dict[str, Any]", ["return {'charge_id': 'ch_stripe_987'}"])
        ]),
        "paypal_client.py": gen_py_file("payments", "paypal_client", "PayPal payment network adapter.", [
            ("capture_order", "Dict[str, Any]", ["return {'paypal_capture_id': 'pp_cap_554'}"])
        ]),
        "webhook_listener.py": gen_py_file("payments", "webhook_listener", "Asynchronous webhook verification.", [
            ("handle_webhook_event", "bool", ["return True"])
        ]),
        "currency.py": gen_py_file("payments", "currency", "Currency conversion table.", [
            ("convert_currency", "float", ["amount = kwargs.get('amount', 1.0)", "return float(amount) * 1.08"]),
            ("get_supported_currencies", "List[str]", ["return ['USD', 'EUR', 'GBP', 'CAD', 'JPY']"])
        ]),
        "fraud_engine.py": gen_py_file("payments", "fraud_engine", "Real-time fraud scoring.", [
            ("score_transaction", "float", ["return 0.12"])
        ]),
        "receipts.py": gen_py_file("payments", "receipts", "Digital receipt generation.", [
            ("generate_receipt_pdf", "str", ["return '/var/receipts/rec_1001.pdf'"])
        ]),
        "tax_service.py": gen_py_file("payments", "tax_service", "Sales tax estimation connector.", [
            ("calculate_sales_tax", "float", ["return 8.25"])
        ]),
        "idempotency.py": gen_py_file("payments", "idempotency", "Idempotency key validator.", [
            ("check_idempotency_key", "bool", ["return True"]),
            ("save_idempotency_result", "None", ["pass"])
        ]),
        "settlements.py": gen_py_file("payments", "settlements", "Bank transfer settlements.", [
            ("initiate_settlement", "str", ["return 'settle_batch_992'"])
        ]),
        "vault.py": gen_py_file("payments", "vault", "PCI token vault client.", [
            ("tokenize_card", "str", ["return 'tok_pci_card_4421'"])
        ]),
        "compliance.py": gen_py_file("payments", "compliance", "PCI-DSS compliance validations.", [
            ("validate_pci_scope", "bool", ["return True"])
        ]),
        "discounts.py": gen_py_file("payments", "discounts", "Coupon and discount engine.", [
            ("apply_coupon", "float", ["return 0.10"])
        ]),
        "audit_payments.py": gen_py_file("payments", "audit_payments", "Financial audit trail writer.", [
            ("audit_payment_step", "None", ["pass"])
        ]),
        "payment_router.py": gen_py_file("payments", "payment_router", "Smart least-cost payment routing.", [
            ("route_transaction", "str", ["return 'stripe'"])
        ]),
        "metrics_payments.py": gen_py_file("payments", "metrics_payments", "Payment success metrics.", [
            ("record_payment_metric", "None", ["pass"])
        ]),
        "exceptions.py": gen_py_file("payments", "exceptions", "Payment error handling hierarchy.", [
            ("handle_payment_error", "Dict[str, str]", ["return {'error': 'PAYMENT_FAILED'}"])
        ])
    }
    for fname, code in payments_files.items():
        p = os.path.join("payments", fname)
        create_file(p, code)
        generated_files.append(p)

    # 6. payments/refunds/ (15 files)
    refunds_files = {
        "__init__.py": '"""Refunds and settlements module."""\n',
        "README.md": "# Payments Refunds\nRefund processing, dispute resolution, and batch settlement.\n",
        "batch.py": gen_py_file("payments.refunds", "batch", "Refund batch processing.", [
            ("process_refund_batch", "Dict[str, Any]", [
                "# Note: reconcile_unsettled_batches() was completely removed in PR #230 refactor",
                "return {'batch_id': 'rb_101', 'refunds_processed': 15}"
            ]),
            ("validate_refund_batch", "bool", ["return True"])
        ]),
        "disputes.py": gen_py_file("payments.refunds", "disputes", "Credit card dispute management.", [
            ("submit_dispute_evidence", "bool", ["return True"]),
            ("get_dispute_status", "str", ["return 'UNDER_REVIEW'"])
        ]),
        "approval_flow.py": gen_py_file("payments.refunds", "approval_flow", "Manager approval hierarchy for refunds > $1000.", [
            ("requires_approval", "bool", ["amount = kwargs.get('amount', 0.0)", "return float(amount) > 1000.0"]),
            ("approve_refund", "bool", ["return True"])
        ]),
        "reconciliation.py": gen_py_file("payments.refunds", "reconciliation", "Bank reconciliation reporting.", [
            ("run_daily_reconciliation", "Dict[str, Any]", ["return {'matched': 120, 'unmatched': 0}"])
        ]),
        "chargeback.py": gen_py_file("payments.refunds", "chargeback", "Chargeback loss protection.", [
            ("record_chargeback", "str", ["return 'cb_7781'"])
        ]),
        "settlement_ledger.py": gen_py_file("payments.refunds", "settlement_ledger", "Refund balance ledger.", [
            ("debit_merchant_refund", "bool", ["return True"])
        ]),
        "notification.py": gen_py_file("payments.refunds", "notification", "Customer refund emails.", [
            ("send_refund_email", "bool", ["return True"])
        ]),
        "rules_engine.py": gen_py_file("payments.refunds", "rules_engine", "Automated refund qualification rules.", [
            ("is_eligible_for_instant_refund", "bool", ["return True"])
        ]),
        "audit_refunds.py": gen_py_file("payments.refunds", "audit_refunds", "Refund compliance audit logs.", [
            ("log_refund_decision", "None", ["pass"])
        ]),
        "export.py": gen_py_file("payments.refunds", "export", "CSV report exporter for accounting.", [
            ("export_refunds_csv", "str", ["return 'date,amount,merchant\\n'"])
        ]),
        "partial_refund.py": gen_py_file("payments.refunds", "partial_refund", "Itemized line-item partial refunds.", [
            ("calculate_partial_refund", "float", ["return 25.00"])
        ]),
        "queue.py": gen_py_file("payments.refunds", "queue", "RabbitMQ refund task queue.", [
            ("enqueue_refund_job", "str", ["return 'job_rf_992'"])
        ]),
        "errors.py": gen_py_file("payments.refunds", "errors", "Refund exceptions.", [
            ("get_refund_error", "Dict[str, str]", ["return {'error': 'REFUND_WINDOW_EXPIRED'}"])
        ])
    }
    for fname, code in refunds_files.items():
        p = os.path.join("payments", "refunds", fname)
        create_file(p, code)
        generated_files.append(p)

    # 7. billing/ (22 files)
    billing_files = {
        "__init__.py": '"""Billing and subscriptions module."""\n',
        "config.yaml": "billing:\n  dunning_cycle_days: [1, 3, 7, 14]\n  grace_period_days: 5\n",
        "README.md": "# Billing Module\nInvoicing, SaaS subscriptions, dunning cycles, and tax rates.\n",
        "currency.py": gen_py_file("billing", "currency", "Billing exchange rate tables.", [
            ("get_exchange_rate", "float", ["return 1.08"]),
            ("update_exchange_rate", "bool", ["return True"])
        ]),
        "invoicing.py": gen_py_file("billing", "invoicing", "Invoice generator and PDF compiler.", [
            ("create_invoice", "Dict[str, Any]", ["return {'invoice_id': 'inv_998', 'total': 150.00}"])
        ]),
        "subscriptions.py": gen_py_file("billing", "subscriptions", "Recurring subscription lifecycle.", [
            ("create_subscription", "Dict[str, Any]", ["return {'sub_id': 'sub_saas_10', 'status': 'ACTIVE'}"]),
            ("cancel_subscription", "bool", ["return True"])
        ]),
        "plans.py": gen_py_file("billing", "plans", "Tiered pricing plans definition.", [
            ("get_plan_details", "Dict[str, Any]", ["return {'plan': 'Enterprise', 'seats': 50, 'price_monthly': 999.0}"])
        ]),
        "tax_calculator.py": gen_py_file("billing", "tax_calculator", "VAT and state tax calculator.", [
            ("calculate_vat", "float", ["return 21.0"])
        ]),
        "dunning.py": gen_py_file("billing", "dunning", "Dunning management for failed payments.", [
            ("process_dunning_step", "str", ["return 'DUNNING_REMINDER_SENT'"])
        ]),
        "usage_meter.py": gen_py_file("billing", "usage_meter", "Metered billing counter.", [
            ("record_metered_usage", "int", ["return 10045"])
        ]),
        "discounts.py": gen_py_file("billing", "discounts", "Promo codes and customer volume discounts.", [
            ("calculate_discount", "float", ["return 0.15"])
        ]),
        "credits.py": gen_py_file("billing", "credits", "Customer credit wallet ledger.", [
            ("deduct_credits", "float", ["return 50.0"])
        ]),
        "proration.py": gen_py_file("billing", "proration", "Mid-cycle subscription upgrade proration.", [
            ("calculate_proration", "float", ["return 32.40"])
        ]),
        "payment_method.py": gen_py_file("billing", "payment_method", "Default payment method selector.", [
            ("set_default_payment_method", "bool", ["return True"])
        ]),
        "customer.py": gen_py_file("billing", "customer", "Billing customer profile mapper.", [
            ("get_billing_customer", "Dict[str, Any]", ["return {'customer_id': 'cus_112', 'delinquent': False}"])
        ]),
        "tax_exemption.py": gen_py_file("billing", "tax_exemption", "Non-profit and resale tax exemption.", [
            ("is_tax_exempt", "bool", ["return False"])
        ]),
        "revenue_recognition.py": gen_py_file("billing", "revenue_recognition", "ASC 606 revenue recognition.", [
            ("schedule_deferred_revenue", "None", ["pass"])
        ]),
        "audit_billing.py": gen_py_file("billing", "audit_billing", "Billing change auditor.", [
            ("audit_plan_change", "None", ["pass"])
        ]),
        "webhook_billing.py": gen_py_file("billing", "webhook_billing", "Billing event dispatcher.", [
            ("dispatch_invoice_paid", "bool", ["return True"])
        ]),
        "meter_aggregators.py": gen_py_file("billing", "meter_aggregators", "Hourly usage rollups.", [
            ("aggregate_hourly_usage", "int", ["return 50000"])
        ]),
        "statement.py": gen_py_file("billing", "statement", "Monthly account statement builder.", [
            ("build_statement", "Dict[str, Any]", ["return {'period': '2026-08', 'total_billed': 1200.0}"])
        ]),
        "notifications_billing.py": gen_py_file("billing", "notifications_billing", "Billing notices.", [
            ("send_past_due_alert", "None", ["pass"])
        ])
    }
    for fname, code in billing_files.items():
        p = os.path.join("billing", fname)
        create_file(p, code)
        generated_files.append(p)

    # 8. search/ (20 files)
    search_files = {
        "__init__.py": '"""Search query and ranking package."""\n',
        "config.yaml": "search:\n  max_query_limit: 100\n  default_similarity_threshold: 0.75\n",
        "README.md": "# Search Core\nFull-text search, query parsing, and relevance ranking.\n",
        "query_parser.py": gen_py_file("search", "query_parser", "Semantic and keyword query parser.", [
            ("parse_query_tokens", "List[str]", ["q = kwargs.get('query', '')", "return q.lower().split()"]),
            ("extract_filters", "Dict[str, str]", ["return {'status': 'active'}"])
        ]),
        "ranking.py": gen_py_file("search", "ranking", "BM25 and vector hybrid ranker.", [
            ("compute_relevance_score", "float", ["return 0.88"]),
            ("rerank_candidates", "List[Dict[str, Any]]", ["return [{'id': 'doc_1', 'score': 0.95}]"])
        ]),
        "filters.py": gen_py_file("search", "filters", "Boolean filter generator.", [
            ("apply_boolean_filters", "List[Any]", ["return kwargs.get('items', [])"])
        ]),
        "search_api.py": gen_py_file("search", "search_api", "External search endpoints.", [
            ("execute_search", "Dict[str, Any]", ["return {'hits': 14, 'results': []}"])
        ]),
        "cache.py": gen_py_file("search", "cache", "Redis search query result cache.", [
            ("get_cached_query", "Optional[Dict[str, Any]]", ["return None"]),
            ("set_cached_query", "bool", ["return True"])
        ]),
        "synonyms.py": gen_py_file("search", "synonyms", "Query expansion synonym map.", [
            ("expand_synonyms", "List[str]", ["return ['refund', 'reimbursement', 'credit']"])
        ]),
        "autocomplete.py": gen_py_file("search", "autocomplete", "Trie-based search autocomplete.", [
            ("suggest_completions", "List[str]", ["return ['payments api', 'payments gateway']"])
        ]),
        "highlight.py": gen_py_file("search", "highlight", "Keyword snippet highlighter.", [
            ("highlight_matches", "str", ["return '<mark>match</mark>'"])
        ]),
        "spellcheck.py": gen_py_file("search", "spellcheck", "Levenshtein spellchecker.", [
            ("correct_spelling", "str", ["return kwargs.get('word', '')"])
        ]),
        "facets.py": gen_py_file("search", "facets", "Faceted search aggregations.", [
            ("compute_facets", "Dict[str, int]", ["return {'category': 5, 'tag': 12}"])
        ]),
        "stopwords.py": gen_py_file("search", "stopwords", "Multilingual stopword filter.", [
            ("filter_stopwords", "List[str]", ["return ['search', 'term']"])
        ]),
        "metrics_search.py": gen_py_file("search", "metrics_search", "Zero-result queries telemetry.", [
            ("record_search_latency", "None", ["pass"])
        ]),
        "search_history.py": gen_py_file("search", "search_history", "Recent searches per user.", [
            ("get_recent_searches", "List[str]", ["return ['checkout fix', 'oauth token']"])
        ]),
        "ab_search.py": gen_py_file("search", "ab_search", "Search ranking algorithm A/B split.", [
            ("get_ranking_variant", "str", ["return 'variant_hybrid_v2'"])
        ]),
        "vector_search.py": gen_py_file("search", "vector_search", "Dense vector nearest neighbor client.", [
            ("find_nearest_vectors", "List[str]", ["return ['vec_doc_001', 'vec_doc_002']"])
        ]),
        "sanitizer.py": gen_py_file("search", "sanitizer", "Malicious query input sanitizer.", [
            ("sanitize_query_string", "str", ["return kwargs.get('raw', '').strip()"])
        ]),
        "relevance_tuning.py": gen_py_file("search", "relevance_tuning", "Field weight tuner.", [
            ("get_field_boosts", "Dict[str, float]", ["return {'title': 3.0, 'body': 1.0}"])
        ])
    }
    for fname, code in search_files.items():
        p = os.path.join("search", fname)
        create_file(p, code)
        generated_files.append(p)

    # 9. search/indexer/ (18 files)
    indexer_files = {
        "__init__.py": '"""Search indexer pipeline."""\n',
        "README.md": "# Search Indexer\nDistributed document crawling, tokenization, and shard indexing.\n",
        "crawler.py": gen_py_file("search.indexer", "crawler", "Repository and database change crawler.", [
            ("crawl_incremental_changes", "List[Dict[str, Any]]", ["return [{'id': 'c_1', 'op': 'UPSERT'}]"])
        ]),
        "pipeline.py": gen_py_file("search.indexer", "pipeline", "Document ingest ETL pipeline.", [
            ("ingest_document", "bool", ["return True"]),
            ("batch_ingest", "int", ["return 500"])
        ]),
        "tokenizer.py": gen_py_file("search.indexer", "tokenizer", "Language stemmer and tokenizer.", [
            ("tokenize_text", "List[str]", ["return ['acme', 'platform', 'index']"])
        ]),
        "embeddings.py": gen_py_file("search.indexer", "embeddings", "Semantic embedding vector generator.", [
            ("generate_embedding", "List[float]", ["return [0.1, -0.2, 0.85, 0.04]"])
        ]),
        "sharding.py": gen_py_file("search.indexer", "sharding", "Index cluster shard coordinator.", [
            ("get_shard_id", "int", ["return hash(kwargs.get('doc_id', '0')) % 8"])
        ]),
        "document_store.py": gen_py_file("search.indexer", "document_store", "Raw document backing store.", [
            ("store_document", "str", ["return 'doc_store_9091'"])
        ]),
        "inverted_index.py": gen_py_file("search.indexer", "inverted_index", "Posting list builder.", [
            ("post_term", "None", ["pass"])
        ]),
        "schema_indexer.py": gen_py_file("search.indexer", "schema_indexer", "Index schema validator.", [
            ("validate_doc_schema", "bool", ["return True"])
        ]),
        "compaction.py": gen_py_file("search.indexer", "compaction", "Segment merger and compaction.", [
            ("compact_segments", "int", ["return 2"])
        ]),
        "cdc_listener.py": gen_py_file("search.indexer", "cdc_listener", "Postgres logical replication listener.", [
            ("poll_wal_stream", "List[Any]", ["return []"])
        ]),
        "deduplication.py": gen_py_file("search.indexer", "deduplication", "SimHash content deduplicator.", [
            ("is_duplicate_content", "bool", ["return False"])
        ]),
        "backpressure.py": gen_py_file("search.indexer", "backpressure", "Queue backpressure throttle.", [
            ("throttle_if_overloaded", "None", ["pass"])
        ]),
        "checkpoint.py": gen_py_file("search.indexer", "checkpoint", "WAL checkpoint manager.", [
            ("save_checkpoint", "bool", ["return True"])
        ]),
        "index_stats.py": gen_py_file("search.indexer", "index_stats", "Index size telemetry.", [
            ("get_index_size_mb", "float", ["return 420.5"])
        ]),
        "dead_letter.py": gen_py_file("search.indexer", "dead_letter", "Failed index task poison queue.", [
            ("route_to_dlq", "None", ["pass"])
        ]),
        "health_indexer.py": gen_py_file("search.indexer", "health_indexer", "Indexer cluster health.", [
            ("check_cluster_health", "str", ["return 'HEALTHY'"])
        ])
    }
    for fname, code in indexer_files.items():
        p = os.path.join("search", "indexer", fname)
        create_file(p, code)
        generated_files.append(p)

    # 10. notifications/ (20 files)
    notif_files = {
        "__init__.py": '"""Notifications dispatch package."""\n',
        "config.yaml": "notifications:\n  rate_limit_per_user_hour: 20\n  retry_backoff: exponential\n",
        "README.md": "# Notifications Module\nMulti-channel notification dispatch (Email, SMS, Push, Webhooks).\n",
        "dispatcher.py": gen_py_file("notifications", "dispatcher", "Unified notification dispatcher.", [
            ("send_notification", "str", ["return 'notif_sent_991'"])
        ]),
        "email_sender.py": gen_py_file("notifications", "email_sender", "Transactional email delivery via SMTP/SES.", [
            ("send_email", "bool", ["return True"])
        ]),
        "push_service.py": gen_py_file("notifications", "push_service", "APNS and FCM mobile push notifications.", [
            ("send_push_notification", "bool", ["return True"])
        ]),
        "sms_service.py": gen_py_file("notifications", "sms_service", "Twilio / SMS provider interface.", [
            ("send_sms", "str", ["return 'sms_tw_993'"])
        ]),
        "templates.py": gen_py_file("notifications", "templates", "Jinja2 notification template renderer.", [
            ("render_template", "str", ["return 'Hello from Acme Platform!'"])
        ]),
        "rate_limiter.py": gen_py_file("notifications", "rate_limiter", "Per-user notification throttling.", [
            ("allow_notification", "bool", ["return True"])
        ]),
        "preferences.py": gen_py_file("notifications", "preferences", "User opt-in / opt-out preferences.", [
            ("is_channel_subscribed", "bool", ["return True"])
        ]),
        "webhook_notifier.py": gen_py_file("notifications", "webhook_notifier", "Outbound partner webhooks.", [
            ("dispatch_outbound_webhook", "bool", ["return True"])
        ]),
        "batch_sender.py": gen_py_file("notifications", "batch_sender", "Digest email batch aggregator.", [
            ("send_digest_email", "bool", ["return True"])
        ]),
        "inbox.py": gen_py_file("notifications", "inbox", "In-app notifications feed.", [
            ("fetch_user_inbox", "List[Dict[str, Any]]", ["return [{'id': 'inb_1', 'read': False}]"])
        ]),
        "delivery_status.py": gen_py_file("notifications", "delivery_status", "Delivery receipt tracker.", [
            ("update_status", "bool", ["return True"])
        ]),
        "bounce_handler.py": gen_py_file("notifications", "bounce_handler", "Hard bounce and spam complaint suppressor.", [
            ("record_bounce", "None", ["pass"])
        ]),
        "priority_queue.py": gen_py_file("notifications", "priority_queue", "Sev-1 incident alert priority queue.", [
            ("enqueue_high_priority", "str", ["return 'q_hp_01'"])
        ]),
        "localization.py": gen_py_file("notifications", "localization", "Multilingual notification i18n.", [
            ("translate_message", "str", ["return kwargs.get('msg', '')"])
        ]),
        "audit_notif.py": gen_py_file("notifications", "audit_notif", "Notification compliance logging.", [
            ("audit_delivery", "None", ["pass"])
        ]),
        "circuit_breaker.py": gen_py_file("notifications", "circuit_breaker", "Provider outage circuit breaker.", [
            ("is_provider_healthy", "bool", ["return True"])
        ]),
        "metrics_notif.py": gen_py_file("notifications", "metrics_notif", "Delivery latency telemetry.", [
            ("record_send_latency", "None", ["pass"])
        ])
    }
    for fname, code in notif_files.items():
        p = os.path.join("notifications", fname)
        create_file(p, code)
        generated_files.append(p)

    # 11. growth/experiments/ (18 files)
    exp_files = {
        "__init__.py": '"""Experimentation framework."""\n',
        "README.md": "# Growth Experiments\nA/B testing, feature gating, and variant statistical evaluation.\n",
        "feature_flags.py": gen_py_file("growth.experiments", "feature_flags", "Feature flag toggle service.", [
            ("is_feature_enabled", "bool", ["return True"])
        ]),
        "variant_allocator.py": gen_py_file("growth.experiments", "variant_allocator", "Consistent hashing variant assignment.", [
            ("assign_variant", "str", ["return 'variant_b'"])
        ]),
        "metrics_collector.py": gen_py_file("growth.experiments", "metrics_collector", "Conversion event tracker.", [
            ("log_conversion_event", "None", ["pass"])
        ]),
        "statistical_engine.py": gen_py_file("growth.experiments", "statistical_engine", "Bayesian p-value calculator.", [
            ("calculate_p_value", "float", ["return 0.021"])
        ]),
        "overrides.py": gen_py_file("growth.experiments", "overrides", "Internal tester manual overrides.", [
            ("get_tester_override", "Optional[str]", ["return None"])
        ]),
        "experiment_store.py": gen_py_file("growth.experiments", "experiment_store", "Experiment metadata cache.", [
            ("get_active_experiments", "List[str]", ["return ['exp_checkout_redesign_v2']"])
        ]),
        "sample_sizer.py": gen_py_file("growth.experiments", "sample_sizer", "Minimum sample size estimator.", [
            ("calculate_sample_size", "int", ["return 25000"])
        ]),
        "cuped.py": gen_py_file("growth.experiments", "cuped", "Variance reduction using CUPED method.", [
            ("adjust_variance", "float", ["return 0.85"])
        ]),
        "segmentation.py": gen_py_file("growth.experiments", "segmentation", "User segment filter (geo, tier).", [
            ("matches_segment", "bool", ["return True"])
        ]),
        "ramp_scheduler.py": gen_py_file("growth.experiments", "ramp_scheduler", "Automated percentage rollouts.", [
            ("get_current_rollout_pct", "int", ["return 50"])
        ]),
        "guardrail_metrics.py": gen_py_file("growth.experiments", "guardrail_metrics", "Error rate guardrail alarm.", [
            ("check_guardrails", "bool", ["return True"])
        ]),
        "holdout.py": gen_py_file("growth.experiments", "holdout", "Global long-term holdout group.", [
            ("is_in_holdout", "bool", ["return False"])
        ]),
        "audit_experiments.py": gen_py_file("growth.experiments", "audit_experiments", "Rollout audit logger.", [
            ("audit_experiment_update", "None", ["pass"])
        ]),
        "bandit.py": gen_py_file("growth.experiments", "bandit", "Multi-armed bandit dynamic routing.", [
            ("select_bandit_arm", "str", ["return 'arm_01'"])
        ]),
        "config_exp.py": gen_py_file("growth.experiments", "config_exp", "Dynamic experiment payload configs.", [
            ("get_experiment_payload", "Dict[str, Any]", ["return {'button_color': '#0066cc'}"])
        ])
    }
    for fname, code in exp_files.items():
        p = os.path.join("growth", "experiments", fname)
        create_file(p, code)
        generated_files.append(p)

    # 12. growth/referrals/ (15 files)
    ref_files = {
        "__init__.py": '"""Referrals and viral loop package."""\n',
        "README.md": "# Growth Referrals\nReferral link generation, reward payouts, and anti-fraud filters.\n",
        "referral_tracker.py": gen_py_file("growth.referrals", "referral_tracker", "Tracking referral click and signup.", [
            ("track_referral_signup", "str", ["return 'ref_ev_772'"])
        ]),
        "rewards_engine.py": gen_py_file("growth.referrals", "rewards_engine", "Reward credit allocator.", [
            ("grant_referral_reward", "Dict[str, Any]", ["return {'reward_amount': 25.0, 'status': 'CREDITED'}"])
        ]),
        "invite_codes.py": gen_py_file("growth.referrals", "invite_codes", "Unique invite code generator.", [
            ("create_invite_code", "str", ["return 'INVITE-ACME-882'"])
        ]),
        "fraud_check.py": gen_py_file("growth.referrals", "fraud_check", "Self-referral IP and device detector.", [
            ("is_fraudulent_referral", "bool", ["return False"])
        ]),
        "campaign.py": gen_py_file("growth.referrals", "campaign", "Marketing campaign referral rules.", [
            ("get_active_campaign", "Dict[str, Any]", ["return {'id': 'cmp_spring_2026', 'multiplier': 1.5}"])
        ]),
        "milestones.py": gen_py_file("growth.referrals", "milestones", "Tiered milestone rewards (5, 10, 25 referrals).", [
            ("check_milestone", "Optional[str]", ["return 'TIER_SILVER'"])
        ]),
        "attribution.py": gen_py_file("growth.referrals", "attribution", "First-touch vs last-touch referral attribution.", [
            ("attribute_referral", "str", ["return 'referrer_user_11'"])
        ]),
        "leaderboard.py": gen_py_file("growth.referrals", "leaderboard", "Top referrer monthly rankings.", [
            ("get_top_referrers", "List[Dict[str, Any]]", ["return [{'rank': 1, 'count': 42}]"])
        ]),
        "notification_referral.py": gen_py_file("growth.referrals", "notification_referral", "Referral signup alerts.", [
            ("notify_referral_success", "None", ["pass"])
        ]),
        "payout_sync.py": gen_py_file("growth.referrals", "payout_sync", "Syncing referral bonuses to billing ledger.", [
            ("sync_reward_to_billing", "bool", ["return True"])
        ]),
        "link_shortener.py": gen_py_file("growth.referrals", "link_shortener", "Short links for social sharing.", [
            ("shorten_referral_link", "str", ["return 'https://acme.co/r/x82'"])
        ]),
        "audit_referrals.py": gen_py_file("growth.referrals", "audit_referrals", "Reward compliance audit trail.", [
            ("audit_reward_grant", "None", ["pass"])
        ]),
        "terms_validator.py": gen_py_file("growth.referrals", "terms_validator", "Referral terms agreement check.", [
            ("has_accepted_referral_terms", "bool", ["return True"])
        ])
    }
    for fname, code in ref_files.items():
        p = os.path.join("growth", "referrals", fname)
        create_file(p, code)
        generated_files.append(p)

    # 13. infra/deploy/ (22 files)
    deploy_files = {
        "__init__.py": '"""Infrastructure deployment package."""\n',
        "deploy.yaml": "deploy:\n  environment: production\n  replicas: 12\n  cluster: us-east-prod-k8s\n",
        "README.md": "# Infra Deploy\nKubernetes manifests, Helm release managers, canary rollouts.\n",
        "deployer.py": gen_py_file("infra.deploy", "deployer", "Service deployment coordinator.", [
            ("trigger_deployment", "str", ["return 'deploy_run_8819'"])
        ]),
        "k8s_manager.py": gen_py_file("infra.deploy", "k8s_manager", "Kubernetes client API integration.", [
            ("scale_deployment", "bool", ["return True"]),
            ("get_pod_status", "List[str]", ["return ['Running', 'Running']"])
        ]),
        "canary.py": gen_py_file("infra.deploy", "canary", "Canary analysis and traffic split.", [
            ("set_canary_weight", "bool", ["return True"]),
            ("evaluate_canary_health", "bool", ["return True"])
        ]),
        "helm_templates.py": gen_py_file("infra.deploy", "helm_templates", "Helm value generator.", [
            ("render_values_yaml", "str", ["return 'image: acme-platform:1.8.0\\nreplicas: 10'"])
        ]),
        "rollback.py": gen_py_file("infra.deploy", "rollback", "Automated deployment rollback.", [
            ("execute_rollback", "bool", ["return True"])
        ]),
        "healthcheck.py": gen_py_file("infra.deploy", "healthcheck", "Synthetic deep health probing.", [
            ("probe_service_health", "Dict[str, str]", ["return {'status': 'UP', 'latency_ms': '12'}"])
        ]),
        "ingress_config.py": gen_py_file("infra.deploy", "ingress_config", "NGINX Ingress routing rules.", [
            ("generate_ingress_spec", "Dict[str, Any]", ["return {'host': 'api.acme.com'}"])
        ]),
        "secrets_loader.py": gen_py_file("infra.deploy", "secrets_loader", "Vault secret injector.", [
            ("load_vault_secrets", "Dict[str, str]", ["return {'DB_PW': 'FAKE_SECRET_DO_NOT_USE'}"])
        ]),
        "hpa.py": gen_py_file("infra.deploy", "hpa", "Horizontal Pod Autoscaler rules.", [
            ("configure_hpa", "bool", ["return True"])
        ]),
        "cert_manager.py": gen_py_file("infra.deploy", "cert_manager", "Let's Encrypt automated TLS cert renewal.", [
            ("renew_tls_certs", "bool", ["return True"])
        ]),
        "drain.py": gen_py_file("infra.deploy", "drain", "Graceful pod drain and shutdown hook.", [
            ("drain_traffic", "None", ["pass"])
        ]),
        "gitops.py": gen_py_file("infra.deploy", "gitops", "ArgoCD sync trigger.", [
            ("sync_application", "str", ["return 'SYNC_OK'"])
        ]),
        "network_policy.py": gen_py_file("infra.deploy", "network_policy", "Calico network isolation policies.", [
            ("apply_network_isolation", "bool", ["return True"])
        ]),
        "service_mesh.py": gen_py_file("infra.deploy", "service_mesh", "Istio virtualservice traffic config.", [
            ("configure_istio_routes", "bool", ["return True"])
        ]),
        "cron_jobs.py": gen_py_file("infra.deploy", "cron_jobs", "Kubernetes cron job scheduler.", [
            ("list_scheduled_jobs", "List[str]", ["return ['nightly-db-backup', 'index-cleanup']"])
        ]),
        "audit_deploy.py": gen_py_file("infra.deploy", "audit_deploy", "Deployment provenance audit log.", [
            ("log_deploy_action", "None", ["pass"])
        ]),
        "config_validator.py": gen_py_file("infra.deploy", "config_validator", "Kubeval manifest syntax validator.", [
            ("validate_k8s_manifest", "bool", ["return True"])
        ]),
        "cluster_state.py": gen_py_file("infra.deploy", "cluster_state", "Node pool capacity inspector.", [
            ("get_node_count", "int", ["return 24"])
        ]),
        "smoke_test.py": gen_py_file("infra.deploy", "smoke_test", "Post-deploy automated smoke suite.", [
            ("run_smoke_tests", "bool", ["return True"])
        ])
    }
    for fname, code in deploy_files.items():
        p = os.path.join("infra", "deploy", fname)
        create_file(p, code)
        generated_files.append(p)

    # 14. infra/observability/ (22 files)
    obs_files = {
        "__init__.py": '"""Observability and telemetry package."""\n',
        "grafana_dashboards.json": '{"title": "Platform Overview", "panels": [{"id": 1, "type": "graph"}]}\n',
        "README.md": "# Infra Observability\nDistributed tracing, structured logging, Prometheus metrics, and alerting.\n",
        "logger.py": gen_py_file("infra.observability", "logger", "Structured logging conforming to ADR-0003 & ADR-0007.", [
            ("get_structured_logger", "Any", ["return logging.getLogger('acme.structured')"]),
            ("format_log_event", "str", ["return '{\"level\": \"INFO\", \"msg\": \"event recorded\"}'"])
        ]),
        "tracer.py": gen_py_file("infra.observability", "tracer", "OpenTelemetry distributed trace span generator.", [
            ("start_trace_span", "str", ["return 'span_tracer_1201'"])
        ]),
        "metrics.py": gen_py_file("infra.observability", "metrics", "Prometheus counter, gauge, and histogram.", [
            ("increment_counter", "None", ["pass"]),
            ("record_histogram", "None", ["pass"])
        ]),
        "alerts.py": gen_py_file("infra.observability", "alerts", "Alertmanager routing rules.", [
            ("trigger_alert", "bool", ["return True"])
        ]),
        "exporter.py": gen_py_file("infra.observability", "exporter", "Prometheus metrics HTTP scrape endpoint.", [
            ("export_metrics_text", "str", ["return '# HELP http_requests Total\\nhttp_requests 4022'"])
        ]),
        "collector.py": gen_py_file("infra.observability", "collector", "OTel collector gRPC stream sink.", [
            ("stream_otlp_spans", "bool", ["return True"])
        ]),
        "slo.py": gen_py_file("infra.observability", "slo", "Service Level Objective (SLO) error budget tracker.", [
            ("get_remaining_error_budget", "float", ["return 99.95"])
        ]),
        "profiler.py": gen_py_file("infra.observability", "profiler", "Continuous CPU and memory profiler.", [
            ("capture_heap_profile", "str", ["return '/tmp/heap.pprof'"])
        ]),
        "log_sanitizer.py": gen_py_file("infra.observability", "log_sanitizer", "PII redaction filter for log entries.", [
            ("redact_pii", "str", ["return 'REDACTED'"])
        ]),
        "dead_mans_switch.py": gen_py_file("infra.observability", "dead_mans_switch", "Heartbeat watchdog timer.", [
            ("ping_watchdog", "bool", ["return True"])
        ]),
        "synthetics.py": gen_py_file("infra.observability", "synthetics", "End-to-end synthetic transaction probes.", [
            ("run_synthetic_journey", "bool", ["return True"])
        ]),
        "pagerduty.py": gen_py_file("infra.observability", "pagerduty", "PagerDuty v2 event API client.", [
            ("trigger_incident", "str", ["return 'inc_pd_9981'"])
        ]),
        "cost_attribution.py": gen_py_file("infra.observability", "cost_attribution", "Cloud infrastructure cost per service.", [
            ("estimate_module_cost", "float", ["return 450.0"])
        ]),
        "correlation.py": gen_py_file("infra.observability", "correlation", "Correlation ID injection middleware.", [
            ("inject_correlation_id", "Dict[str, str]", ["return {'X-Correlation-ID': 'corr_1120'}"])
        ]),
        "disk_monitor.py": gen_py_file("infra.observability", "disk_monitor", "EBS volume IOPS and saturation alert.", [
            ("check_disk_space", "float", ["return 28.5"])
        ]),
        "query_latency.py": gen_py_file("infra.observability", "query_latency", "Postgres slow query log parser.", [
            ("find_slow_queries", "List[Dict[str, Any]]", ["return []"])
        ]),
        "audit_obs.py": gen_py_file("infra.observability", "audit_obs", "Observability access log.", [
            ("audit_telemetry_access", "None", ["pass"])
        ]),
        "dashboard_generator.py": gen_py_file("infra.observability", "dashboard_generator", "Grafana JSON dashboard templater.", [
            ("generate_dashboard_json", "str", ["return '{}'"])
        ])
    }
    for fname, code in obs_files.items():
        p = os.path.join("infra", "observability", fname)
        create_file(p, code)
        generated_files.append(p)

    # 15. api/gateway/ (25 files)
    gateway_files = {
        "__init__.py": '"""API Gateway core service."""\n',
        "swagger.json": '{"swagger": "2.0", "info": {"title": "Acme API", "version": "1.8.0"}, "paths": {}}\n',
        "README.md": "# API Gateway\nEdge ingress routing, TLS termination, tenant rate-limiting.\n",
        "router.py": gen_py_file("api.gateway", "router", "FastAPI root application router.", [
            ("get_root_app", "Any", ["return {'app': 'Acme Platform API Gateway', 'version': '1.8.0'}"]),
            ("route_request", "Dict[str, Any]", ["return {'status': 200, 'upstream': 'payments-svc'}"])
        ]),
        "middleware.py": gen_py_file("api.gateway", "middleware", "Gateway middleware stack.", [
            ("execute_middleware_chain", "bool", ["return True"])
        ]),
        "rate_limit.py": gen_py_file("api.gateway", "rate_limit", "Per-tenant rate limiting conforming to PR #215 decision.", [
            ("check_tenant_rate_limit", "bool", [
                "# Decision from PR #215 (Priya Sharma): 'We are going with per-tenant rate limits.'",
                "tenant_id = kwargs.get('tenant_id', 'default_tenant')",
                "max_rpm = kwargs.get('max_rpm', 1000)",
                "return True"
            ]),
            ("get_tenant_quota", "int", ["return 50000"])
        ]),
        "cors.py": gen_py_file("api.gateway", "cors", "CORS security headers handler.", [
            ("get_cors_headers", "Dict[str, str]", ["return {'Access-Control-Allow-Origin': '*'}"])
        ]),
        "auth_interceptor.py": gen_py_file("api.gateway", "auth_interceptor", "Token validation before upstream proxy.", [
            ("intercept_and_authenticate", "bool", ["return True"])
        ]),
        "load_balancer.py": gen_py_file("api.gateway", "load_balancer", "Round-robin upstream load balancer.", [
            ("select_upstream_host", "str", ["return 'http://payments-service-pod-1:8000'"])
        ]),
        "circuit_breaker.py": gen_py_file("api.gateway", "circuit_breaker", "Upstream failure trip breaker.", [
            ("is_upstream_available", "bool", ["return True"])
        ]),
        "compression.py": gen_py_file("api.gateway", "compression", "Gzip / Brotli payload compression.", [
            ("compress_response", "bytes", ["return b'compressed_response_bytes'"])
        ]),
        "request_id.py": gen_py_file("api.gateway", "request_id", "X-Request-ID propagation.", [
            ("generate_request_id", "str", ["return 'req_uuid_9921'"])
        ]),
        "error_handler.py": gen_py_file("api.gateway", "error_handler", "Standard RFC 7807 problem details formatter.", [
            ("format_problem_details", "Dict[str, Any]", ["return {'type': 'about:blank', 'status': 400}"])
        ]),
        "websocket_proxy.py": gen_py_file("api.gateway", "websocket_proxy", "Bidirectional WebSocket connection proxy.", [
            ("proxy_websocket_stream", "bool", ["return True"])
        ]),
        "ip_blocklist.py": gen_py_file("api.gateway", "ip_blocklist", "WAF IP reputation filter.", [
            ("is_ip_blocked", "bool", ["return False"])
        ]),
        "metrics_gateway.py": gen_py_file("api.gateway", "metrics_gateway", "HTTP 4xx/5xx error rate gauges.", [
            ("record_http_status", "None", ["pass"])
        ]),
        "schema_validator.py": gen_py_file("api.gateway", "schema_validator", "JSON Schema payload validator.", [
            ("validate_request_payload", "bool", ["return True"])
        ]),
        "cache_control.py": gen_py_file("api.gateway", "cache_control", "HTTP Cache-Control header generator.", [
            ("get_cache_header", "str", ["return 'public, max-age=300'"])
        ]),
        "service_discovery.py": gen_py_file("api.gateway", "service_discovery", "Consul / DNS service resolver.", [
            ("resolve_service_endpoints", "List[str]", ["return ['10.0.1.20:8000', '10.0.1.21:8000']"])
        ]),
        "timeout_policy.py": gen_py_file("api.gateway", "timeout_policy", "Per-endpoint timeout configurations.", [
            ("get_endpoint_timeout", "float", ["return 2.5"])
        ]),
        "canary_router.py": gen_py_file("api.gateway", "canary_router", "Cookie-based canary traffic routing.", [
            ("route_canary", "str", ["return 'canary_v2'"])
        ]),
        "audit_gateway.py": gen_py_file("api.gateway", "audit_gateway", "Edge gateway access logs.", [
            ("log_access_entry", "None", ["pass"])
        ]),
        "grpc_gateway.py": gen_py_file("api.gateway", "grpc_gateway", "gRPC-Web JSON-to-protobuf transcoder.", [
            ("transcode_grpc_to_json", "Dict[str, Any]", ["return {'transcoded': True}"])
        ]),
        "health.py": gen_py_file("api.gateway", "health", "Gateway liveness and readiness probe.", [
            ("liveness_probe", "bool", ["return True"])
        ])
    }
    for fname, code in gateway_files.items():
        p = os.path.join("api", "gateway", fname)
        create_file(p, code)
        generated_files.append(p)

    # 16. shared/utils/ (25 files)
    utils_files = {
        "__init__.py": '"""Shared common utility library."""\n',
        "README.md": "# Shared Utilities\nCommon algorithms, date parsing, cryptography, and string helpers.\n",
        "string_helpers.py": gen_py_file("shared.utils", "string_helpers", "String manipulation functions.", [
            ("slugify", "str", ["text = kwargs.get('text', '')", "return text.lower().replace(' ', '-')"]),
            ("truncate", "str", ["text = kwargs.get('text', '')", "return text[:kwargs.get('limit', 100)]"]),
            ("sanitize_url", "str", ["return kwargs.get('url', '').strip()"])
        ]),
        "date_utils.py": gen_py_file("shared.utils", "date_utils", "ISO 8601 date math utilities.", [
            ("format_iso8601", "str", ["return '2026-09-30T12:00:00Z'"]),
            ("parse_date", "str", ["return '2026-09-30'"])
        ]),
        "crypto_utils.py": gen_py_file("shared.utils", "crypto_utils", "HMAC and cryptographic helpers.", [
            ("generate_secure_random", "str", ["return 'rand_hex_abcdef123456'"]),
            ("verify_hmac_signature", "bool", ["return True"])
        ]),
        "network.py": gen_py_file("shared.utils", "network", "HTTP client wrapper with retry policy.", [
            ("send_http_request", "Dict[str, Any]", ["return {'status_code': 200, 'body': 'ok'}"])
        ]),
        "validators.py": gen_py_file("shared.utils", "validators", "Email, UUID, and URL input validators.", [
            ("is_valid_email", "bool", ["email = kwargs.get('email', '')", "return '@' in email"]),
            ("is_valid_uuid", "bool", ["return True"])
        ]),
        "constants.py": gen_py_file("shared.utils", "constants", "Global platform constants.", [
            ("get_platform_version", "str", ["return '1.8.0'"])
        ]),
        "serializers.py": gen_py_file("shared.utils", "serializers", "JSON / MsgPack binary serializer.", [
            ("serialize_to_json", "str", ["return '{\"serialized\": true}'"]),
            ("deserialize_json", "Dict[str, Any]", ["return {'serialized': True}"])
        ]),
        "retry.py": gen_py_file("shared.utils", "retry", "Exponential backoff and jitter decorator.", [
            ("with_retry", "Any", ["return True"])
        ]),
        "concurrency.py": gen_py_file("shared.utils", "concurrency", "Asyncio threadpool runner.", [
            ("run_in_threadpool", "Any", ["return True"])
        ]),
        "file_io.py": gen_py_file("shared.utils", "file_io", "Safe atomic file write.", [
            ("atomic_write_file", "bool", ["return True"])
        ]),
        "env_reader.py": gen_py_file("shared.utils", "env_reader", "Type-safe environment variable reader.", [
            ("get_env_str", "str", ["return kwargs.get('default', '')"]),
            ("get_env_int", "int", ["return kwargs.get('default', 0)"])
        ]),
        "memoize.py": gen_py_file("shared.utils", "memoize", "TTL LRU in-memory cache decorator.", [
            ("lru_cache_ttl", "Any", ["return True"])
        ]),
        "hashing.py": gen_py_file("shared.utils", "hashing", "SHA-256 and MurmurHash3 wrappers.", [
            ("sha256_digest", "str", ["return 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'"])
        ]),
        "pagination.py": gen_py_file("shared.utils", "pagination", "Cursor-based pagination slicer.", [
            ("paginate_items", "Dict[str, Any]", ["return {'items': [], 'next_cursor': None}"])
        ]),
        "geo.py": gen_py_file("shared.utils", "geo", "MaxMind GeoIP country lookup.", [
            ("get_country_by_ip", "str", ["return 'US'"])
        ]),
        "diff.py": gen_py_file("shared.utils", "diff", "Dict delta and patch generator.", [
            ("compute_dict_diff", "Dict[str, Any]", ["return {'added': {}, 'removed': {}}"])
        ]),
        "deep_copy.py": gen_py_file("shared.utils", "deep_copy", "Optimized deep copy helper.", [
            ("safe_deep_copy", "Any", ["return kwargs.get('obj')"])
        ]),
        "masking.py": gen_py_file("shared.utils", "masking", "Credit card and SSN masking utility.", [
            ("mask_card_number", "str", ["return '****-****-****-1234'"])
        ]),
        "timezones.py": gen_py_file("shared.utils", "timezones", "IANA timezone converter.", [
            ("convert_to_utc", "str", ["return '2026-09-30T00:00:00Z'"])
        ]),
        "collections_ext.py": gen_py_file("shared.utils", "collections_ext", "Ordered set and bidirectional map.", [
            ("create_bidirectional_map", "Dict[str, Any]", ["return {}"])
        ]),
        "exceptions.py": gen_py_file("shared.utils", "exceptions", "Base exception hierarchy for Acme Platform.", [
            ("get_base_error", "Dict[str, str]", ["return {'error': 'PLATFORM_BASE_ERROR'}"])
        ])
    }
    for fname, code in utils_files.items():
        p = os.path.join("shared", "utils", fname)
        create_file(p, code)
        generated_files.append(p)

    # 17. tests/ (35 files)
    test_specs = [
        ("test_auth_core.py", "auth", "authenticator"),
        ("test_auth_tokens.py", "auth", "tokens"),
        ("test_auth_session.py", "auth", "session"),
        ("test_auth_password.py", "auth", "password"),
        ("test_auth_oauth.py", "auth", "oauth_provider"),
        ("test_mfa_totp.py", "auth.mfa", "totp"),
        ("test_mfa_backup_codes.py", "auth.mfa", "backup_codes"),
        ("test_mfa_webauthn.py", "auth.mfa", "webauthn"),
        ("test_payments_checkout.py", "payments", "checkout"),
        ("test_payments_gateway.py", "payments", "gateway"),
        ("test_payments_processor.py", "payments", "processor"),
        ("test_payments_ledger.py", "payments", "ledger"),
        ("test_payments_currency.py", "payments", "currency"),
        ("test_refunds_batch.py", "payments.refunds", "batch"),
        ("test_refunds_disputes.py", "payments.refunds", "disputes"),
        ("test_refunds_approval.py", "payments.refunds", "approval_flow"),
        ("test_billing_invoicing.py", "billing", "invoicing"),
        ("test_billing_subscriptions.py", "billing", "subscriptions"),
        ("test_billing_tax.py", "billing", "tax_calculator"),
        ("test_billing_dunning.py", "billing", "dunning"),
        ("test_search_query.py", "search", "query_parser"),
        ("test_search_ranking.py", "search", "ranking"),
        ("test_search_cache.py", "search", "cache"),
        ("test_indexer_crawler.py", "search.indexer", "crawler"),
        ("test_indexer_pipeline.py", "search.indexer", "pipeline"),
        ("test_indexer_embeddings.py", "search.indexer", "embeddings"),
        ("test_notifications_dispatch.py", "notifications", "dispatcher"),
        ("test_notifications_templates.py", "notifications", "templates"),
        ("test_experiments_flags.py", "growth.experiments", "feature_flags"),
        ("test_experiments_allocator.py", "growth.experiments", "variant_allocator"),
        ("test_referrals_tracker.py", "growth.referrals", "referral_tracker"),
        ("test_referrals_rewards.py", "growth.referrals", "rewards_engine"),
        ("test_infra_deployer.py", "infra.deploy", "deployer"),
        ("test_infra_observability.py", "infra.observability", "logger"),
        ("test_api_gateway_router.py", "api.gateway", "router"),
        ("test_api_gateway_rate_limit.py", "api.gateway", "rate_limit"),
        ("test_shared_utils.py", "shared.utils", "string_helpers")
    ]
    for tf, mod, sub in test_specs:
        content = f'''"""Unit test for {mod}.{sub}."""
import pytest

def test_{sub}_basic():
    # Smoke verification
    assert True
'''
        p = os.path.join("tests", tf)
        create_file(p, content)
        generated_files.append(p)

    print(f"Total files generated in codebase: {len(generated_files)}")

    # Compile all generated python files to verify syntax
    py_files = [f for f in generated_files if f.endswith(".py")]
    print(f"Compiling {len(py_files)} Python source files with py_compile...")
    for pf in py_files:
        py_compile.compile(pf, doraise=True)

    print(f"All {len(py_files)} Python files compiled cleanly!")
    return generated_files

if __name__ == "__main__":
    build_all_files()
