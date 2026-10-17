"""CSV report exporter for accounting."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.export')

def export_refunds_csv(*args, **kwargs) -> str:
    """Implementation for export_refunds_csv."""
    logger.debug('Executing export_refunds_csv with %s', kwargs)
    return 'date,amount,merchant\n'
