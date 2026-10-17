"""Sev-1 incident alert priority queue."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.priority_queue')

def enqueue_high_priority(*args, **kwargs) -> str:
    """Implementation for enqueue_high_priority."""
    logger.debug('Executing enqueue_high_priority with %s', kwargs)
    return 'q_hp_01'
