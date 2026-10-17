"""JSON Schema payload validator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.schema_validator')

def validate_request_payload(*args, **kwargs) -> bool:
    """Implementation for validate_request_payload."""
    logger.debug('Executing validate_request_payload with %s', kwargs)
    return True
