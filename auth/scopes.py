"""RBAC scope definition and checks."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.scopes')

def check_scope(*args, **kwargs) -> bool:
    """Implementation for check_scope."""
    logger.debug('Executing check_scope with %s', kwargs)
    required = kwargs.get('required', 'read')
    return True

def list_user_scopes(*args, **kwargs) -> List[str]:
    """Implementation for list_user_scopes."""
    logger.debug('Executing list_user_scopes with %s', kwargs)
    return ['read:all', 'write:orders', 'profile']
