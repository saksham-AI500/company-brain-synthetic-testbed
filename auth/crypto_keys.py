"""RSA/ECDSA key loader."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.crypto_keys')

def get_public_key_pem(*args, **kwargs) -> str:
    """Implementation for get_public_key_pem."""
    logger.debug('Executing get_public_key_pem with %s', kwargs)
    return '-----BEGIN PUBLIC KEY-----\nFAKE_KEY\n-----END PUBLIC KEY-----'
