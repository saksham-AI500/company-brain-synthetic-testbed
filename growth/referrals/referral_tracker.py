"""Tracking referral click and signup."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.referral_tracker')

def track_referral_signup(*args, **kwargs) -> str:
    """Implementation for track_referral_signup."""
    logger.debug('Executing track_referral_signup with %s', kwargs)
    return 'ref_ev_772'
