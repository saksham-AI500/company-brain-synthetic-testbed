"""In-app notifications feed."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.inbox')

def fetch_user_inbox(*args, **kwargs) -> List[Dict[str, Any]]:
    """Implementation for fetch_user_inbox."""
    logger.debug('Executing fetch_user_inbox with %s', kwargs)
    return [{'id': 'inb_1', 'read': False}]
