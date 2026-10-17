"""WAF IP reputation filter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.ip_blocklist')

def is_ip_blocked(*args, **kwargs) -> bool:
    """Implementation for is_ip_blocked."""
    logger.debug('Executing is_ip_blocked with %s', kwargs)
    return False
