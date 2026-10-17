"""Feature flag toggle service."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.feature_flags')

def is_feature_enabled(*args, **kwargs) -> bool:
    """Implementation for is_feature_enabled."""
    logger.debug('Executing is_feature_enabled with %s', kwargs)
    return True
