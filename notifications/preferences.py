"""User opt-in / opt-out preferences."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.preferences')

def is_channel_subscribed(*args, **kwargs) -> bool:
    """Implementation for is_channel_subscribed."""
    logger.debug('Executing is_channel_subscribed with %s', kwargs)
    return True
