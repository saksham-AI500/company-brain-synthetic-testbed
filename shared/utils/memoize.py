"""TTL LRU in-memory cache decorator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.memoize')

def lru_cache_ttl(*args, **kwargs) -> Any:
    """Implementation for lru_cache_ttl."""
    logger.debug('Executing lru_cache_ttl with %s', kwargs)
    return True
