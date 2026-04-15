import hashlib
import time
from enum import Enum
from typing import Dict, Optional

class ChainType(Enum):
    ETHEREUM = "ETH"
    BSC = "BSC"
    SOLANA = "SOL"

class CrossChainBridge:
    def __init__(self):
        self.transactions: Dict[str, Dict] = {}
        self.chain_validators = {
            ChainType.ETHEREUM: "0xValidator1",
            ChainType.BSC: "0xValidator2",
            ChainType.SOLANA: "0xValidator3"
        }

    def create_bridge_tx(self, from_chain: ChainType, to_chain: ChainType, sender: str, recipient: str, amount: float) -> str:
        tx_id = hashlib.sha256(f"{from_chain}{to_chain}{sender}{amount}{time()}".encode()).hexdigest()
        
        self.transactions[tx_id] = {
            "tx_id": tx_id,
            "from_chain": from_chain.value,
            "to_chain": to_chain.value,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "status": "pending",
            "timestamp": time()
        }
        return tx_id

    def validate_transaction(self, tx_id: str, validator: str) -> bool:
        if tx_id not in self.transactions:
            return False
        tx = self.transactions[tx_id]
        if validator not in self.chain_validators.values():
            return False
        
        tx["status"] = "validated"
        return True

    def complete_bridge(self, tx_id: str) -> bool:
        if tx_id not in self.transactions:
            return False
        if self.transactions[tx_id]["status"] != "validated":
            return False
        
        self.transactions[tx_id]["status"] = "completed"
        return True

    def get_tx_status(self, tx_id: str) -> Optional[str]:
        return self.transactions.get(tx_id, {}).get("status")
