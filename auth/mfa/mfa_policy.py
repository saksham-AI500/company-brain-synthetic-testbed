"""MFA enforcement policies."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.mfa_policy')

def is_mfa_required(*args, **kwargs) -> bool:
    """Implementation for is_mfa_required."""
    logger.debug('Executing is_mfa_required with %s', kwargs)
    return True

def get_supported_factors(*args, **kwargs) -> List[str]:
    """Implementation for get_supported_factors."""
    logger.debug('Executing get_supported_factors with %s', kwargs)
    return ['totp', 'webauthn', 'backup_code']
