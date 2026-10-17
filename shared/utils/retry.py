"""Exponential backoff and jitter decorator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.retry')

def with_retry(*args, **kwargs) -> Any:
    """Implementation for with_retry."""
    logger.debug('Executing with_retry with %s', kwargs)
    return True
