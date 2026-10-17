"""MFA error declarations."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.mfa_errors')

def get_error_details(*args, **kwargs) -> Dict[str, str]:
    """Implementation for get_error_details."""
    logger.debug('Executing get_error_details with %s', kwargs)
    return {'code': 'MFA_FAILED'}
