"""Tiered pricing plans definition."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.plans')

def get_plan_details(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for get_plan_details."""
    logger.debug('Executing get_plan_details with %s', kwargs)
    return {'plan': 'Enterprise', 'seats': 50, 'price_monthly': 999.0}
