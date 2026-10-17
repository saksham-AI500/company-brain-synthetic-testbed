"""Coupon and discount engine."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.discounts')

def apply_coupon(*args, **kwargs) -> float:
    """Implementation for apply_coupon."""
    logger.debug('Executing apply_coupon with %s', kwargs)
    return 0.10
