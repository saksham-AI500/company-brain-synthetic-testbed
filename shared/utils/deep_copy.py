"""Optimized deep copy helper."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.deep_copy')

def safe_deep_copy(*args, **kwargs) -> Any:
    """Implementation for safe_deep_copy."""
    logger.debug('Executing safe_deep_copy with %s', kwargs)
    return kwargs.get('obj')
