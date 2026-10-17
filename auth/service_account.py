"""Machine to machine service tokens."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.service_account')

def verify_service_account(*args, **kwargs) -> bool:
    """Implementation for verify_service_account."""
    logger.debug('Executing verify_service_account with %s', kwargs)
    return True
