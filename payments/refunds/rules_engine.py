"""Automated refund qualification rules."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.rules_engine')

def is_eligible_for_instant_refund(*args, **kwargs) -> bool:
    """Implementation for is_eligible_for_instant_refund."""
    logger.debug('Executing is_eligible_for_instant_refund with %s', kwargs)
    return True
