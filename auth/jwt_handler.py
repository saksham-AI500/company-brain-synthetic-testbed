"""JSON Web Token encoder and decoder."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.jwt_handler')

def encode_claims(*args, **kwargs) -> str:
    """Implementation for encode_claims."""
    logger.debug('Executing encode_claims with %s', kwargs)
    return 'header.claims.signed'

def decode_claims(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for decode_claims."""
    logger.debug('Executing decode_claims with %s', kwargs)
    return {'claims': {'aud': 'acme-api'}}
