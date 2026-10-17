"""Experiment metadata cache."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.experiment_store')

def get_active_experiments(*args, **kwargs) -> List[str]:
    """Implementation for get_active_experiments."""
    logger.debug('Executing get_active_experiments with %s', kwargs)
    return ['exp_checkout_redesign_v2']
