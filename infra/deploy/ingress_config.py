"""NGINX Ingress routing rules."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.ingress_config')

def generate_ingress_spec(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for generate_ingress_spec."""
    logger.debug('Executing generate_ingress_spec with %s', kwargs)
    return {'host': 'api.acme.com'}
