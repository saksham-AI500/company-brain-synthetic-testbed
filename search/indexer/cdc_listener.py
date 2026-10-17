"""Postgres logical replication listener."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.cdc_listener')

def poll_wal_stream(*args, **kwargs) -> List[Any]:
    """Implementation for poll_wal_stream."""
    logger.debug('Executing poll_wal_stream with %s', kwargs)
    return []
