"""Tiered milestone rewards (5, 10, 25 referrals)."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.milestones')

def check_milestone(*args, **kwargs) -> Optional[str]:
    """Implementation for check_milestone."""
    logger.debug('Executing check_milestone with %s', kwargs)
    return 'TIER_SILVER'
