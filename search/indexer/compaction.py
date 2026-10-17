"""Segment merger and compaction."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.compaction')

def compact_segments(*args, **kwargs) -> int:
    """Implementation for compact_segments."""
    logger.debug('Executing compact_segments with %s', kwargs)
    return 2
