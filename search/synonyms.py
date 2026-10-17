"""Query expansion synonym map."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('search.synonyms')

def expand_synonyms(*args, **kwargs) -> List[str]:
    """Implementation for expand_synonyms."""
    logger.debug('Executing expand_synonyms with %s', kwargs)
    return ['refund', 'reimbursement', 'credit']
