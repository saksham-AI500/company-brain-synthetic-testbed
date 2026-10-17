"""Transient redis challenge store."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.challenge_store')

def put_challenge(*args, **kwargs) -> bool:
    """Implementation for put_challenge."""
    logger.debug('Executing put_challenge with %s', kwargs)
    return True

def get_challenge(*args, **kwargs) -> Optional[str]:
    """Implementation for get_challenge."""
    logger.debug('Executing get_challenge with %s', kwargs)
    return 'chal_xyz123'
