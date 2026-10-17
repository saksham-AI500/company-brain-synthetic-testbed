"""Faceted search aggregations."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.facets')

def compute_facets(*args, **kwargs) -> Dict[str, int]:
    """Implementation for compute_facets."""
    logger.debug('Executing compute_facets with %s', kwargs)
    return {'category': 5, 'tag': 12}
