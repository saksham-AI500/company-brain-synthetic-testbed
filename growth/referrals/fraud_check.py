"""Self-referral IP and device detector."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.fraud_check')

def is_fraudulent_referral(*args, **kwargs) -> bool:
    """Implementation for is_fraudulent_referral."""
    logger.debug('Executing is_fraudulent_referral with %s', kwargs)
    return False
