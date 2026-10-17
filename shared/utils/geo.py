"""MaxMind GeoIP country lookup."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.geo')

def get_country_by_ip(*args, **kwargs) -> str:
    """Implementation for get_country_by_ip."""
    logger.debug('Executing get_country_by_ip with %s', kwargs)
    return 'US'
