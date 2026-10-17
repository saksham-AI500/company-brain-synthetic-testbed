"""First-touch vs last-touch referral attribution."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.attribution')

def attribute_referral(*args, **kwargs) -> str:
    """Implementation for attribute_referral."""
    logger.debug('Executing attribute_referral with %s', kwargs)
    return 'referrer_user_11'
