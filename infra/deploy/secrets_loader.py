"""Vault secret injector."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.secrets_loader')

def load_vault_secrets(*args, **kwargs) -> Dict[str, str]:
    """Implementation for load_vault_secrets."""
    logger.debug('Executing load_vault_secrets with %s', kwargs)
    return {'DB_PW': 'FAKE_SECRET_DO_NOT_USE'}
