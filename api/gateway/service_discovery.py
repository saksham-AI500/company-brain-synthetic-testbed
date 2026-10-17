"""Consul / DNS service resolver."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.service_discovery')

def resolve_service_endpoints(*args, **kwargs) -> List[str]:
    """Implementation for resolve_service_endpoints."""
    logger.debug('Executing resolve_service_endpoints with %s', kwargs)
    return ['10.0.1.20:8000', '10.0.1.21:8000']
