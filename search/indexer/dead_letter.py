"""Failed index task poison queue."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.dead_letter')

def route_to_dlq(*args, **kwargs) -> None:
    """Implementation for route_to_dlq."""
    logger.debug('Executing route_to_dlq with %s', kwargs)
    pass
