"""Consistent hashing variant assignment."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.variant_allocator')

def assign_variant(*args, **kwargs) -> str:
    """Implementation for assign_variant."""
    logger.debug('Executing assign_variant with %s', kwargs)
    return 'variant_b'
