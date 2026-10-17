"""Search ranking algorithm A/B split."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.ab_search')

def get_ranking_variant(*args, **kwargs) -> str:
    """Implementation for get_ranking_variant."""
    logger.debug('Executing get_ranking_variant with %s', kwargs)
    return 'variant_hybrid_v2'
