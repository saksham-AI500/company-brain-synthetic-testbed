"""RabbitMQ refund task queue."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('payments.refunds.queue')

def enqueue_refund_job(*args, **kwargs) -> str:
    """Implementation for enqueue_refund_job."""
    logger.debug('Executing enqueue_refund_job with %s', kwargs)
    return 'job_rf_992'
