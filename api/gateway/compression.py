"""Gzip / Brotli payload compression."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('api.gateway.compression')

def compress_response(*args, **kwargs) -> bytes:
    """Implementation for compress_response."""
    logger.debug('Executing compress_response with %s', kwargs)
    return b'compressed_response_bytes'
