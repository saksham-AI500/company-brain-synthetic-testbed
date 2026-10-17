"""Non-profit and resale tax exemption."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.tax_exemption')

def is_tax_exempt(*args, **kwargs) -> bool:
    """Implementation for is_tax_exempt."""
    logger.debug('Executing is_tax_exempt with %s', kwargs)
    return False
