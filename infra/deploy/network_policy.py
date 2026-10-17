"""Calico network isolation policies."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.network_policy')

def apply_network_isolation(*args, **kwargs) -> bool:
    """Implementation for apply_network_isolation."""
    logger.debug('Executing apply_network_isolation with %s', kwargs)
    return True
