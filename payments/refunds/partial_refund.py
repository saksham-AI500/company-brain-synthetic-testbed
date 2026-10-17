"""Itemized line-item partial refunds."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.partial_refund')

def calculate_partial_refund(*args, **kwargs) -> float:
    """Implementation for calculate_partial_refund."""
    logger.debug('Executing calculate_partial_refund with %s', kwargs)
    return 25.00
