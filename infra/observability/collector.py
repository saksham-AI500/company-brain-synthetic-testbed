"""OTel collector gRPC stream sink."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.collector')

def stream_otlp_spans(*args, **kwargs) -> bool:
    """Implementation for stream_otlp_spans."""
    logger.debug('Executing stream_otlp_spans with %s', kwargs)
    return True
