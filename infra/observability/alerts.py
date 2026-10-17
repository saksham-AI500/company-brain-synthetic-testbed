"""Alertmanager routing rules."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.alerts')

def trigger_alert(*args, **kwargs) -> bool:
    """Implementation for trigger_alert."""
    logger.debug('Executing trigger_alert with %s', kwargs)
    return True
