"""Outbound partner webhooks."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.webhook_notifier')

def dispatch_outbound_webhook(*args, **kwargs) -> bool:
    """Implementation for dispatch_outbound_webhook."""
    logger.debug('Executing dispatch_outbound_webhook with %s', kwargs)
    return True
