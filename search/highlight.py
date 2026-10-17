"""Keyword snippet highlighter."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.highlight')

def highlight_matches(*args, **kwargs) -> str:
    """Implementation for highlight_matches."""
    logger.debug('Executing highlight_matches with %s', kwargs)
    return '<mark>match</mark>'
