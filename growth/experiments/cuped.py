"""Variance reduction using CUPED method."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.cuped')

def adjust_variance(*args, **kwargs) -> float:
    """Implementation for adjust_variance."""
    logger.debug('Executing adjust_variance with %s', kwargs)
    return 0.85
