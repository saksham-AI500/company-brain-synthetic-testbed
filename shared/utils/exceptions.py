"""Base exception hierarchy for Acme Platform."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.exceptions')

def get_base_error(*args, **kwargs) -> Dict[str, str]:
    """Implementation for get_base_error."""
    logger.debug('Executing get_base_error with %s', kwargs)
    return {'error': 'PLATFORM_BASE_ERROR'}
