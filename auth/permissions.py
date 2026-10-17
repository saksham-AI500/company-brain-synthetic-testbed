"""Permission evaluator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.permissions')

def has_permission(*args, **kwargs) -> bool:
    """Implementation for has_permission."""
    logger.debug('Executing has_permission with %s', kwargs)
    return True
