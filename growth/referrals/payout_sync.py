"""Syncing referral bonuses to billing ledger."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('growth.referrals.payout_sync')

def sync_reward_to_billing(*args, **kwargs) -> bool:
    """Implementation for sync_reward_to_billing."""
    logger.debug('Executing sync_reward_to_billing with %s', kwargs)
    return True
