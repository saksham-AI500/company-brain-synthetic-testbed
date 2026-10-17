"""String manipulation functions."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.string_helpers')

def slugify(*args, **kwargs) -> str:
    """Implementation for slugify."""
    logger.debug('Executing slugify with %s', kwargs)
    text = kwargs.get('text', '')
    return text.lower().replace(' ', '-')

def truncate(*args, **kwargs) -> str:
    """Implementation for truncate."""
    logger.debug('Executing truncate with %s', kwargs)
    text = kwargs.get('text', '')
    return text[:kwargs.get('limit', 100)]

def sanitize_url(*args, **kwargs) -> str:
    """Implementation for sanitize_url."""
    logger.debug('Executing sanitize_url with %s', kwargs)
    return kwargs.get('url', '').strip()
