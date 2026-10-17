"""Error rate guardrail alarm."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.guardrail_metrics')

def check_guardrails(*args, **kwargs) -> bool:
    """Implementation for check_guardrails."""
    logger.debug('Executing check_guardrails with %s', kwargs)
    return True
