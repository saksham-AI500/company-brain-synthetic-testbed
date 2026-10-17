"""Twilio / SMS provider interface."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.sms_service')

def send_sms(*args, **kwargs) -> str:
    """Implementation for send_sms."""
    logger.debug('Executing send_sms with %s', kwargs)
    return 'sms_tw_993'
