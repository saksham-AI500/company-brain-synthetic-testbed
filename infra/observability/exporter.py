"""Prometheus metrics HTTP scrape endpoint."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.exporter')

def export_metrics_text(*args, **kwargs) -> str:
    """Implementation for export_metrics_text."""
    logger.debug('Executing export_metrics_text with %s', kwargs)
    return '# HELP http_requests Total\nhttp_requests 4022'
