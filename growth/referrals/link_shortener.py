"""Short links for social sharing."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.link_shortener')

def shorten_referral_link(*args, **kwargs) -> str:
    """Implementation for shorten_referral_link."""
    logger.debug('Executing shorten_referral_link with %s', kwargs)
    return 'https://acme.co/r/x82'
