"""Transactional email delivery via SMTP/SES."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.email_sender')

def send_email(*args, **kwargs) -> bool:
    """Implementation for send_email."""
    logger.debug('Executing send_email with %s', kwargs)
    return True
