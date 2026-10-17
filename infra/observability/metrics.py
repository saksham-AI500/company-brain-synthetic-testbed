"""Prometheus counter, gauge, and histogram."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.metrics')

def increment_counter(*args, **kwargs) -> None:
    """Implementation for increment_counter."""
    logger.debug('Executing increment_counter with %s', kwargs)
    pass

def record_histogram(*args, **kwargs) -> None:
    """Implementation for record_histogram."""
    logger.debug('Executing record_histogram with %s', kwargs)
    pass
