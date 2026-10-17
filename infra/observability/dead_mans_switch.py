"""Heartbeat watchdog timer."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.dead_mans_switch')

def ping_watchdog(*args, **kwargs) -> bool:
    """Implementation for ping_watchdog."""
    logger.debug('Executing ping_watchdog with %s', kwargs)
    return True
