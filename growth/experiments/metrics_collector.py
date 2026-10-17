"""Conversion event tracker."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.metrics_collector')

def log_conversion_event(*args, **kwargs) -> None:
    """Implementation for log_conversion_event."""
    logger.debug('Executing log_conversion_event with %s', kwargs)
    pass
