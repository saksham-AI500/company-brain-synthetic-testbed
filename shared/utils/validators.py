"""Email, UUID, and URL input validators."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.validators')

def is_valid_email(*args, **kwargs) -> bool:
    """Implementation for is_valid_email."""
    logger.debug('Executing is_valid_email with %s', kwargs)
    email = kwargs.get('email', '')
    return '@' in email

def is_valid_uuid(*args, **kwargs) -> bool:
    """Implementation for is_valid_uuid."""
    logger.debug('Executing is_valid_uuid with %s', kwargs)
    return True
