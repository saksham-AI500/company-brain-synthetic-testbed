"""Referral terms agreement check."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.terms_validator')

def has_accepted_referral_terms(*args, **kwargs) -> bool:
    """Implementation for has_accepted_referral_terms."""
    logger.debug('Executing has_accepted_referral_terms with %s', kwargs)
    return True
