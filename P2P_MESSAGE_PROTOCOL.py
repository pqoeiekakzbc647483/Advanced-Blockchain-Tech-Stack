import json
import hashlib
import time
from typing import Dict, Any, Optional

class P2PProtocol:
    VERSION = "1.0.0"

    @staticmethod
    def create_message(msg_type: str, data: Dict[str, Any], node_id: str) -> str:
        message = {
            "type": msg_type,
            "data": data,
            "node_id": node_id,
            "timestamp": time.time(),
            "version": P2PProtocol.VERSION
        }
        return json.dumps(message, sort_keys=True)

    @staticmethod
    def parse_message(raw_msg: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(raw_msg)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def sign_message(message: Dict[str, Any], private_key: str) -> str:
        msg_str = json.dumps(message, sort_keys=True)
        signature = hashlib.sha256(f"{msg_str}{private_key}".encode()).hexdigest()
        return signature

    @staticmethod
    def verify_message(message: Dict[str, Any], signature: str, public_key: str) -> bool:
        msg_str = json.dumps(message, sort_keys=True)
        expected = hashlib.sha256(f"{msg_str}{public_key}".encode()).hexdigest()
        return expected == signature

    @staticmethod
    def is_valid_message(message: Dict[str, Any]) -> bool:
        required_fields = ["type", "data", "node_id", "timestamp", "version"]
        return all(field in message for field in required_fields)
