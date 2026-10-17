"""Customer refund emails."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.notification')

def send_refund_email(*args, **kwargs) -> bool:
    """Implementation for send_refund_email."""
    logger.debug('Executing send_refund_email with %s', kwargs)
    return True
