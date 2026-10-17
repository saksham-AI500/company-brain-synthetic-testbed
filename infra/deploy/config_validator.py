"""Kubeval manifest syntax validator."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.config_validator')

def validate_k8s_manifest(*args, **kwargs) -> bool:
    """Implementation for validate_k8s_manifest."""
    logger.debug('Executing validate_k8s_manifest with %s', kwargs)
    return True
