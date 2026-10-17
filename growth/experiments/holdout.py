"""Global long-term holdout group."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.holdout')

def is_in_holdout(*args, **kwargs) -> bool:
    """Implementation for is_in_holdout."""
    logger.debug('Executing is_in_holdout with %s', kwargs)
    return False
