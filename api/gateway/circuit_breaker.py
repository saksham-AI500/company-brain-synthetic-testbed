"""Upstream failure trip breaker."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.circuit_breaker')

def is_upstream_available(*args, **kwargs) -> bool:
    """Implementation for is_upstream_available."""
    logger.debug('Executing is_upstream_available with %s', kwargs)
    return True
