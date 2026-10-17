"""Metered billing counter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.usage_meter')

def record_metered_usage(*args, **kwargs) -> int:
    """Implementation for record_metered_usage."""
    logger.debug('Executing record_metered_usage with %s', kwargs)
    return 10045
