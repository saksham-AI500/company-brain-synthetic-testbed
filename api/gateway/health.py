"""Gateway liveness and readiness probe."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.health')

def liveness_probe(*args, **kwargs) -> bool:
    """Implementation for liveness_probe."""
    logger.debug('Executing liveness_probe with %s', kwargs)
    return True
