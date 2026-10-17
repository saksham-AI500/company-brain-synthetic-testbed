"""APNS and FCM mobile push notifications."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.push_service')

def send_push_notification(*args, **kwargs) -> bool:
    """Implementation for send_push_notification."""
    logger.debug('Executing send_push_notification with %s', kwargs)
    return True
