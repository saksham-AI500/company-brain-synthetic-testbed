"""Custom token claims mapper."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.claims_mapper')

def map_tenant_claims(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for map_tenant_claims."""
    logger.debug('Executing map_tenant_claims with %s', kwargs)
    return {'tenant_id': 'ten_99'}
