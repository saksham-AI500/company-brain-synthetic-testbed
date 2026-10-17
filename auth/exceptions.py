"""Auth specific exceptions."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.exceptions')

def raise_unauthorized(*args, **kwargs) -> None:
    """Implementation for raise_unauthorized."""
    logger.debug('Executing raise_unauthorized with %s', kwargs)
    raise PermissionError('Unauthorized access attempt')
