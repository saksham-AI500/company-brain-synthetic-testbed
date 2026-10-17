"""Provider outage circuit breaker."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.circuit_breaker')

def is_provider_healthy(*args, **kwargs) -> bool:
    """Implementation for is_provider_healthy."""
    logger.debug('Executing is_provider_healthy with %s', kwargs)
    return True
