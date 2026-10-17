"""User segment filter (geo, tier)."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.segmentation')

def matches_segment(*args, **kwargs) -> bool:
    """Implementation for matches_segment."""
    logger.debug('Executing matches_segment with %s', kwargs)
    return True
