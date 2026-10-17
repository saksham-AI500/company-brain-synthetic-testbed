"""Raw document backing store."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.document_store')

def store_document(*args, **kwargs) -> str:
    """Implementation for store_document."""
    logger.debug('Executing store_document with %s', kwargs)
    return 'doc_store_9091'
