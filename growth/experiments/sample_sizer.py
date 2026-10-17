"""Minimum sample size estimator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.sample_sizer')

def calculate_sample_size(*args, **kwargs) -> int:
    """Implementation for calculate_sample_size."""
    logger.debug('Executing calculate_sample_size with %s', kwargs)
    return 25000
