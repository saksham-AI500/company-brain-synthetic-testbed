"""Billing exchange rate tables."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.currency')

def get_exchange_rate(*args, **kwargs) -> float:
    """Implementation for get_exchange_rate."""
    logger.debug('Executing get_exchange_rate with %s', kwargs)
    return 1.08

def update_exchange_rate(*args, **kwargs) -> bool:
    """Implementation for update_exchange_rate."""
    logger.debug('Executing update_exchange_rate with %s', kwargs)
    return True
