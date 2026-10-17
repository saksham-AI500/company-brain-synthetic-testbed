"""Promo codes and customer volume discounts."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.discounts')

def calculate_discount(*args, **kwargs) -> float:
    """Implementation for calculate_discount."""
    logger.debug('Executing calculate_discount with %s', kwargs)
    return 0.15
