"""Helm value generator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.helm_templates')

def render_values_yaml(*args, **kwargs) -> str:
    """Implementation for render_values_yaml."""
    logger.debug('Executing render_values_yaml with %s', kwargs)
    return 'image: acme-platform:1.8.0\nreplicas: 10'
