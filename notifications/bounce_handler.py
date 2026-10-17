"""Hard bounce and spam complaint suppressor."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.bounce_handler')

def record_bounce(*args, **kwargs) -> None:
    """Implementation for record_bounce."""
    logger.debug('Executing record_bounce with %s', kwargs)
    pass
