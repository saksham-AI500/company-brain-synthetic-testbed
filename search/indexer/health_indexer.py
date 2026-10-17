"""Indexer cluster health."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.health_indexer')

def check_cluster_health(*args, **kwargs) -> str:
    """Implementation for check_cluster_health."""
    logger.debug('Executing check_cluster_health with %s', kwargs)
    return 'HEALTHY'
