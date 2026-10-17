"""Refund balance ledger."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.settlement_ledger')

def debit_merchant_refund(*args, **kwargs) -> bool:
    """Implementation for debit_merchant_refund."""
    logger.debug('Executing debit_merchant_refund with %s', kwargs)
    return True
