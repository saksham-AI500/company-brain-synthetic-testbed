"""Token revocation bloom filter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.revocation_list')

def is_revoked(*args, **kwargs) -> bool:
    """Implementation for is_revoked."""
    logger.debug('Executing is_revoked with %s', kwargs)
    return False
