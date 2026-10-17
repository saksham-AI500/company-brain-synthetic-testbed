"""Currency conversion table."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.currency')

def convert_currency(*args, **kwargs) -> float:
    """Implementation for convert_currency."""
    logger.debug('Executing convert_currency with %s', kwargs)
    amount = kwargs.get('amount', 1.0)
    return float(amount) * 1.08

def get_supported_currencies(*args, **kwargs) -> List[str]:
    """Implementation for get_supported_currencies."""
    logger.debug('Executing get_supported_currencies with %s', kwargs)
    return ['USD', 'EUR', 'GBP', 'CAD', 'JPY']
