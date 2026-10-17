"""Asyncio threadpool runner."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.concurrency')

def run_in_threadpool(*args, **kwargs) -> Any:
    """Implementation for run_in_threadpool."""
    logger.debug('Executing run_in_threadpool with %s', kwargs)
    return True
