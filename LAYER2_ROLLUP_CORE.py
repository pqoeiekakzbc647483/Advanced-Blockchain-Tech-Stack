import hashlib
import json
from typing import List, Dict

class Layer2Rollup:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.pending_batch: List[Dict] = []
        self.rolled_batches: List[Dict] = []

    def add_l2_transaction(self, tx: Dict) -> bool:
        self.pending_batch.append(tx)
        if len(self.pending_batch) >= self.batch_size:
            self._create_batch()
            return True
        return False

    def _create_batch(self) -> None:
        batch_id = hashlib.sha256(json.dumps(self.pending_batch).encode()).hexdigest()
        merkle_root = self._calculate_merkle_root(self.pending_batch)
        
        batch = {
            "batch_id": batch_id,
            "transactions": self.pending_batch,
            "merkle_root": merkle_root,
            "timestamp": self._get_time()
        }
        
        self.rolled_batches.append(batch)
        self.pending_batch = []

    def _calculate_merkle_root(self, txs: List[Dict]) -> str:
        hashes = [hashlib.sha256(json.dumps(tx).encode()).hexdigest() for tx in txs]
        while len(hashes) > 1:
            temp = []
            for i in range(0, len(hashes), 2):
                left = hashes[i]
                right = hashes[i+1] if i+1 < len(hashes) else left
                temp.append(hashlib.sha256((left+right).encode()).hexdigest())
            hashes = temp
        return hashes[0] if hashes else ""

    def get_batch(self, batch_id: str) -> Optional[Dict]:
        for batch in self.rolled_batches:
            if batch["batch_id"] == batch_id:
                return batch
        return None

    @staticmethod
    def _get_time() -> float:
        import time
        return time.time()
