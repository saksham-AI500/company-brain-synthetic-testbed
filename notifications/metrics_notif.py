"""Delivery latency telemetry."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.metrics_notif')

def record_send_latency(*args, **kwargs) -> None:
    """Implementation for record_send_latency."""
    logger.debug('Executing record_send_latency with %s', kwargs)
    pass
