"""CORS security headers handler."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.cors')

def get_cors_headers(*args, **kwargs) -> Dict[str, str]:
    """Implementation for get_cors_headers."""
    logger.debug('Executing get_cors_headers with %s', kwargs)
    return {'Access-Control-Allow-Origin': '*'}
