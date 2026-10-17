"""HTTP 4xx/5xx error rate gauges."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.metrics_gateway')

def record_http_status(*args, **kwargs) -> None:
    """Implementation for record_http_status."""
    logger.debug('Executing record_http_status with %s', kwargs)
    pass
