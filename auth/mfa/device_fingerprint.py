"""Trusted device registration."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.device_fingerprint')

def is_device_trusted(*args, **kwargs) -> bool:
    """Implementation for is_device_trusted."""
    logger.debug('Executing is_device_trusted with %s', kwargs)
    return True
