"""Per-endpoint timeout configurations."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.timeout_policy')

def get_endpoint_timeout(*args, **kwargs) -> float:
    """Implementation for get_endpoint_timeout."""
    logger.debug('Executing get_endpoint_timeout with %s', kwargs)
    return 2.5
