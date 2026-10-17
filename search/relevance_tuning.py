"""Field weight tuner."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.relevance_tuning')

def get_field_boosts(*args, **kwargs) -> Dict[str, float]:
    """Implementation for get_field_boosts."""
    logger.debug('Executing get_field_boosts with %s', kwargs)
    return {'title': 3.0, 'body': 1.0}
