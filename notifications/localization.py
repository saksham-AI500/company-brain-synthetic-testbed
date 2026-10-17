"""Multilingual notification i18n."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('notifications.localization')

def translate_message(*args, **kwargs) -> str:
    """Implementation for translate_message."""
    logger.debug('Executing translate_message with %s', kwargs)
    return kwargs.get('msg', '')
