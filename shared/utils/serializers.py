"""JSON / MsgPack binary serializer."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('shared.utils.serializers')

def serialize_to_json(*args, **kwargs) -> str:
    """Implementation for serialize_to_json."""
    logger.debug('Executing serialize_to_json with %s', kwargs)
    return '{"serialized": true}'

def deserialize_json(*args, **kwargs) -> Dict[str, Any]:
    """Implementation for deserialize_json."""
    logger.debug('Executing deserialize_json with %s', kwargs)
    return {'serialized': True}
