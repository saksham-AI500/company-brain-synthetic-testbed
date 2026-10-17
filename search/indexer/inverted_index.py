"""Posting list builder."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.inverted_index')

def post_term(*args, **kwargs) -> None:
    """Implementation for post_term."""
    logger.debug('Executing post_term with %s', kwargs)
    pass
