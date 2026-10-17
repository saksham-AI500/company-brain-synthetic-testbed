"""Document ingest ETL pipeline."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.indexer.pipeline')

def ingest_document(*args, **kwargs) -> bool:
    """Implementation for ingest_document."""
    logger.debug('Executing ingest_document with %s', kwargs)
    return True

def batch_ingest(*args, **kwargs) -> int:
    """Implementation for batch_ingest."""
    logger.debug('Executing batch_ingest with %s', kwargs)
    return 500
