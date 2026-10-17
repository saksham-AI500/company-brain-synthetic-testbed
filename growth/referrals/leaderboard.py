"""Top referrer monthly rankings."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.leaderboard')

def get_top_referrers(*args, **kwargs) -> List[Dict[str, Any]]:
    """Implementation for get_top_referrers."""
    logger.debug('Executing get_top_referrers with %s', kwargs)
    return [{'rank': 1, 'count': 42}]
