"""Index schema validator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.schema_indexer')

def validate_doc_schema(*args, **kwargs) -> bool:
    """Implementation for validate_doc_schema."""
    logger.debug('Executing validate_doc_schema with %s', kwargs)
    return True
