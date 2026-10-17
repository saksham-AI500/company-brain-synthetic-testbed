"""Language stemmer and tokenizer."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.tokenizer')

def tokenize_text(*args, **kwargs) -> List[str]:
    """Implementation for tokenize_text."""
    logger.debug('Executing tokenize_text with %s', kwargs)
    return ['acme', 'platform', 'index']
