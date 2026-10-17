"""PayPal payment network adapter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.paypal_client')

def capture_order(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for capture_order."""
    logger.debug('Executing capture_order with %s', kwargs)
    return {'paypal_capture_id': 'pp_cap_554'}
