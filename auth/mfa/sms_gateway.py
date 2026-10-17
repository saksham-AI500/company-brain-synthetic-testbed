"""SMS dispatch for 2FA."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.sms_gateway')

def send_verification_sms(*args, **kwargs) -> str:
    """Implementation for send_verification_sms."""
    logger.debug('Executing send_verification_sms with %s', kwargs)
    return 'sms_msg_98213'
