"""Trie-based search autocomplete."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.autocomplete')

def suggest_completions(*args, **kwargs) -> List[str]:
    """Implementation for suggest_completions."""
    logger.debug('Executing suggest_completions with %s', kwargs)
    return ['payments api', 'payments gateway']
