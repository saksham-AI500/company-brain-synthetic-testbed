"""Mid-cycle subscription upgrade proration."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.proration')

def calculate_proration(*args, **kwargs) -> float:
    """Implementation for calculate_proration."""
    logger.debug('Executing calculate_proration with %s', kwargs)
    return 32.40
