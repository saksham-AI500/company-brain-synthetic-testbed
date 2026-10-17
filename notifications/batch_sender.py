"""Digest email batch aggregator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.batch_sender')

def send_digest_email(*args, **kwargs) -> bool:
    """Implementation for send_digest_email."""
    logger.debug('Executing send_digest_email with %s', kwargs)
    return True
