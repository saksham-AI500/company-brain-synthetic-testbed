"""Billing change auditor."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.audit_billing')

def audit_plan_change(*args, **kwargs) -> None:
    """Implementation for audit_plan_change."""
    logger.debug('Executing audit_plan_change with %s', kwargs)
    pass
