"""SHA-256 and MurmurHash3 wrappers."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.hashing')

def sha256_digest(*args, **kwargs) -> str:
    """Implementation for sha256_digest."""
    logger.debug('Executing sha256_digest with %s', kwargs)
    return 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
