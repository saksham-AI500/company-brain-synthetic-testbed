"""Credit card and SSN masking utility."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.masking')

def mask_card_number(*args, **kwargs) -> str:
    """Implementation for mask_card_number."""
    logger.debug('Executing mask_card_number with %s', kwargs)
    return '****-****-****-1234'
