"""Index cluster shard coordinator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.sharding')

def get_shard_id(*args, **kwargs) -> int:
    """Implementation for get_shard_id."""
    logger.debug('Executing get_shard_id with %s', kwargs)
    return hash(kwargs.get('doc_id', '0')) % 8
