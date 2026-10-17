"""Notifications for MFA state changes."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('auth.mfa.mfa_notifier')

def notify_factor_enrolled(*args, **kwargs) -> None:
    """Implementation for notify_factor_enrolled."""
    logger.debug('Executing notify_factor_enrolled with %s', kwargs)
    logger.info('Factor enrolled: %s', kwargs)
