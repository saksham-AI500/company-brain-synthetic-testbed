"""Zero-result queries telemetry."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.metrics_search')

def record_search_latency(*args, **kwargs) -> None:
    """Implementation for record_search_latency."""
    logger.debug('Executing record_search_latency with %s', kwargs)
    pass
