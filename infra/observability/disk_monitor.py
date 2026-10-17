"""EBS volume IOPS and saturation alert."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('infra.observability.disk_monitor')

def check_disk_space(*args, **kwargs) -> float:
    """Implementation for check_disk_space."""
    logger.debug('Executing check_disk_space with %s', kwargs)
    return 28.5
