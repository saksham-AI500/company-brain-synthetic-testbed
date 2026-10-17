"""Queue backpressure throttle."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.backpressure')

def throttle_if_overloaded(*args, **kwargs) -> None:
    """Implementation for throttle_if_overloaded."""
    logger.debug('Executing throttle_if_overloaded with %s', kwargs)
    pass
