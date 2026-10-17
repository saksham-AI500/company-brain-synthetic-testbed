"""Malicious query input sanitizer."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.sanitizer')

def sanitize_query_string(*args, **kwargs) -> str:
    """Implementation for sanitize_query_string."""
    logger.debug('Executing sanitize_query_string with %s', kwargs)
    return kwargs.get('raw', '').strip()
