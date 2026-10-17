"""Dynamic experiment payload configs."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.experiments.config_exp')

def get_experiment_payload(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for get_experiment_payload."""
    logger.debug('Executing get_experiment_payload with %s', kwargs)
    return {'button_color': '#0066cc'}
