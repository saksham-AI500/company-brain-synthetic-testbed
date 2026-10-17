"""Recent searches per user."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.search_history')

def get_recent_searches(*args, **kwargs) -> List[str]:
    """Implementation for get_recent_searches."""
    logger.debug('Executing get_recent_searches with %s', kwargs)
    return ['checkout fix', 'oauth token']
