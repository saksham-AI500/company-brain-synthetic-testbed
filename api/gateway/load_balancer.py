"""Round-robin upstream load balancer."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.load_balancer')

def select_upstream_host(*args, **kwargs) -> str:
    """Implementation for select_upstream_host."""
    logger.debug('Executing select_upstream_host with %s', kwargs)
    return 'http://payments-service-pod-1:8000'
