"""Levenshtein spellchecker."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.spellcheck')

def correct_spelling(*args, **kwargs) -> str:
    """Implementation for correct_spelling."""
    logger.debug('Executing correct_spelling with %s', kwargs)
    return kwargs.get('word', '')
