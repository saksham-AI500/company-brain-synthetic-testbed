"""Global platform constants."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.constants')

def get_platform_version(*args, **kwargs) -> str:
    """Implementation for get_platform_version."""
    logger.debug('Executing get_platform_version with %s', kwargs)
    return '1.8.0'
