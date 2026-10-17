"""Continuous CPU and memory profiler."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.profiler')

def capture_heap_profile(*args, **kwargs) -> str:
    """Implementation for capture_heap_profile."""
    logger.debug('Executing capture_heap_profile with %s', kwargs)
    return '/tmp/heap.pprof'
