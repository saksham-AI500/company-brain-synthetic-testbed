"""Graceful pod drain and shutdown hook."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.drain')

def drain_traffic(*args, **kwargs) -> None:
    """Implementation for drain_traffic."""
    logger.debug('Executing drain_traffic with %s', kwargs)
    pass
