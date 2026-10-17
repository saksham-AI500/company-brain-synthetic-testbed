"""Referral signup alerts."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.notification_referral')

def notify_referral_success(*args, **kwargs) -> None:
    """Implementation for notify_referral_success."""
    logger.debug('Executing notify_referral_success with %s', kwargs)
    pass
