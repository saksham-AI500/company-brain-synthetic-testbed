"""Multi-armed bandit dynamic routing."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.bandit')

def select_bandit_arm(*args, **kwargs) -> str:
    """Implementation for select_bandit_arm."""
    logger.debug('Executing select_bandit_arm with %s', kwargs)
    return 'arm_01'
