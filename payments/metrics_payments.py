"""Payment success metrics."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.metrics_payments')

def record_payment_metric(*args, **kwargs) -> None:
    """Implementation for record_payment_metric."""
    logger.debug('Executing record_payment_metric with %s', kwargs)
    pass
