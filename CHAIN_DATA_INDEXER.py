from typing import List, Dict, Any
from collections import defaultdict

class ChainDataIndexer:
    def __init__(self):
        self.address_index = defaultdict(list)
        self.tx_index = {}
        self.block_index = {}

    def index_block(self, block: Dict[str, Any]) -> None:
        block_height = block["index"]
        self.block_index[block_height] = block
        
        for tx in block.get("transactions", []):
            tx_id = tx.get("tx_id")
            if tx_id:
                self.tx_index[tx_id] = {"block_height": block_height, "data": tx}
                
                sender = tx.get("sender")
                recipient = tx.get("recipient")
                if sender:
                    self.address_index[sender].append({"type": "sent", "tx_id": tx_id, "height": block_height})
                if recipient:
                    self.address_index[recipient].append({"type": "received", "tx_id": tx_id, "height": block_height})

    def index_chain(self, chain: List[Dict[str, Any]]) -> None:
        for block in chain:
            self.index_block(block)

    def get_transactions_by_address(self, address: str) -> List[Dict[str, Any]]:
        return self.address_index.get(address, [])

    def get_transaction(self, tx_id: str) -> Dict[str, Any]:
        return self.tx_index.get(tx_id, {})

    def get_block_by_height(self, height: int) -> Dict[str, Any]:
        return self.block_index.get(height, {})

    def clear_index(self) -> None:
        self.address_index.clear()
        self.tx_index.clear()
        self.block_index.clear()
