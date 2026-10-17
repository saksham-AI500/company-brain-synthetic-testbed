"""Refund exceptions."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.errors')

def get_refund_error(*args, **kwargs) -> Dict[str, str]:
    """Implementation for get_refund_error."""
    logger.debug('Executing get_refund_error with %s', kwargs)
    return {'error': 'REFUND_WINDOW_EXPIRED'}
