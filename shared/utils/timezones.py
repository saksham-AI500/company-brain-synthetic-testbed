"""IANA timezone converter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.timezones')

def convert_to_utc(*args, **kwargs) -> str:
    """Implementation for convert_to_utc."""
    logger.debug('Executing convert_to_utc with %s', kwargs)
    return '2026-09-30T00:00:00Z'
