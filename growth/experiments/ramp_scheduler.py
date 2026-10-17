"""Automated percentage rollouts."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.ramp_scheduler')

def get_current_rollout_pct(*args, **kwargs) -> int:
    """Implementation for get_current_rollout_pct."""
    logger.debug('Executing get_current_rollout_pct with %s', kwargs)
    return 50
