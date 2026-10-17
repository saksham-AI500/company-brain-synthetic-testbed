"""Marketing campaign referral rules."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.campaign')

def get_active_campaign(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for get_active_campaign."""
    logger.debug('Executing get_active_campaign with %s', kwargs)
    return {'id': 'cmp_spring_2026', 'multiplier': 1.5}
