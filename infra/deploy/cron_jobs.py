"""Kubernetes cron job scheduler."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.deploy.cron_jobs')

def list_scheduled_jobs(*args, **kwargs) -> List[str]:
    """Implementation for list_scheduled_jobs."""
    logger.debug('Executing list_scheduled_jobs with %s', kwargs)
    return ['nightly-db-backup', 'index-cleanup']
