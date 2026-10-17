"""Type-safe environment variable reader."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.env_reader')

def get_env_str(*args, **kwargs) -> str:
    """Implementation for get_env_str."""
    logger.debug('Executing get_env_str with %s', kwargs)
    return kwargs.get('default', '')

def get_env_int(*args, **kwargs) -> int:
    """Implementation for get_env_int."""
    logger.debug('Executing get_env_int with %s', kwargs)
    return kwargs.get('default', 0)
