"""Billing notices."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.notifications_billing')

def send_past_due_alert(*args, **kwargs) -> None:
    """Implementation for send_past_due_alert."""
    logger.debug('Executing send_past_due_alert with %s', kwargs)
    pass
