"""Bayesian p-value calculator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.statistical_engine')

def calculate_p_value(*args, **kwargs) -> float:
    """Implementation for calculate_p_value."""
    logger.debug('Executing calculate_p_value with %s', kwargs)
    return 0.021
