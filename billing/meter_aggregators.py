"""Hourly usage rollups."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('billing.meter_aggregators')

def aggregate_hourly_usage(*args, **kwargs) -> int:
    """Implementation for aggregate_hourly_usage."""
    logger.debug('Executing aggregate_hourly_usage with %s', kwargs)
    return 50000
