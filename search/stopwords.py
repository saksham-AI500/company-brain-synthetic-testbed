"""Multilingual stopword filter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.stopwords')

def filter_stopwords(*args, **kwargs) -> List[str]:
    """Implementation for filter_stopwords."""
    logger.debug('Executing filter_stopwords with %s', kwargs)
    return ['search', 'term']
