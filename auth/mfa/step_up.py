"""Step-up authentication for high risk actions."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.step_up')

def require_step_up(*args, **kwargs) -> bool:
    """Implementation for require_step_up."""
    logger.debug('Executing require_step_up with %s', kwargs)
    return True
