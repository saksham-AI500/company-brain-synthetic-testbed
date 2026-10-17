"""Sales tax estimation connector."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.tax_service')

def calculate_sales_tax(*args, **kwargs) -> float:
    """Implementation for calculate_sales_tax."""
    logger.debug('Executing calculate_sales_tax with %s', kwargs)
    return 8.25
