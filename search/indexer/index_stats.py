"""Index size telemetry."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.index_stats')

def get_index_size_mb(*args, **kwargs) -> float:
    """Implementation for get_index_size_mb."""
    logger.debug('Executing get_index_size_mb with %s', kwargs)
    return 420.5
