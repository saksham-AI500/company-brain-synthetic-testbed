"""HTTP Cache-Control header generator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.cache_control')

def get_cache_header(*args, **kwargs) -> str:
    """Implementation for get_cache_header."""
    logger.debug('Executing get_cache_header with %s', kwargs)
    return 'public, max-age=300'
