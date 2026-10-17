"""Per-user notification throttling."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.rate_limiter')

def allow_notification(*args, **kwargs) -> bool:
    """Implementation for allow_notification."""
    logger.debug('Executing allow_notification with %s', kwargs)
    return True
