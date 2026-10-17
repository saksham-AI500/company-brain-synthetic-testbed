"""Internal tester manual overrides."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.overrides')

def get_tester_override(*args, **kwargs) -> Optional[str]:
    """Implementation for get_tester_override."""
    logger.debug('Executing get_tester_override with %s', kwargs)
    return None
