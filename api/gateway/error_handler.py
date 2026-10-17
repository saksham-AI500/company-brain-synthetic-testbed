"""Standard RFC 7807 problem details formatter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.error_handler')

def format_problem_details(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for format_problem_details."""
    logger.debug('Executing format_problem_details with %s', kwargs)
    return {'type': 'about:blank', 'status': 400}
