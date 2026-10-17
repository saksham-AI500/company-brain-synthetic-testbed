"""Hardware security key attestation."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.fido_attestation')

def verify_attestation(*args, **kwargs) -> bool:
    """Implementation for verify_attestation."""
    logger.debug('Executing verify_attestation with %s', kwargs)
    return True
