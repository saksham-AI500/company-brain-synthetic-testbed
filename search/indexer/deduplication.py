"""SimHash content deduplicator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.deduplication')

def is_duplicate_content(*args, **kwargs) -> bool:
    """Implementation for is_duplicate_content."""
    logger.debug('Executing is_duplicate_content with %s', kwargs)
    return False
