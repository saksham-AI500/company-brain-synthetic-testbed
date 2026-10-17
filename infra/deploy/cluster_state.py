"""Node pool capacity inspector."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.cluster_state')

def get_node_count(*args, **kwargs) -> int:
    """Implementation for get_node_count."""
    logger.debug('Executing get_node_count with %s', kwargs)
    return 24
