"""Stripe payment network adapter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.stripe_client')

def create_charge(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for create_charge."""
    logger.debug('Executing create_charge with %s', kwargs)
    return {'charge_id': 'ch_stripe_987'}
