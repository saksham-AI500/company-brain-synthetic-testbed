"""Edge gateway access logs."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.audit_gateway')

def log_access_entry(*args, **kwargs) -> None:
    """Implementation for log_access_entry."""
    logger.debug('Executing log_access_entry with %s', kwargs)
    pass
