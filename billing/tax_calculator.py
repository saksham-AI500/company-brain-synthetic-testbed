"""VAT and state tax calculator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.tax_calculator')

def calculate_vat(*args, **kwargs) -> float:
    """Implementation for calculate_vat."""
    logger.debug('Executing calculate_vat with %s', kwargs)
    return 21.0
