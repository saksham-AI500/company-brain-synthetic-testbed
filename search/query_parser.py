"""Semantic and keyword query parser."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.query_parser')

def parse_query_tokens(*args, **kwargs) -> List[str]:
    """Implementation for parse_query_tokens."""
    logger.debug('Executing parse_query_tokens with %s', kwargs)
    q = kwargs.get('query', '')
    return q.lower().split()

def extract_filters(*args, **kwargs) -> Dict[str, str]:
    """Implementation for extract_filters."""
    logger.debug('Executing extract_filters with %s', kwargs)
    return {'status': 'active'}
