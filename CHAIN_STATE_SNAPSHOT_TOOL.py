import json
import hashlib
import time
from typing import List, Dict, Any

class StateSnapshot:
    def __init__(self, blockchain: List[Dict[str, Any]]):
        self.chain = blockchain
        self.snapshots: List[Dict[str, Any]] = []

    def create_snapshot(self, snapshot_name: str) -> str:
        snapshot_data = {
            "name": snapshot_name,
            "timestamp": time.time(),
            "block_height": len(self.chain),
            "chain_state": self._get_current_state(),
            "pending_txs": self._get_pending_transactions()
        }

        snapshot_id = hashlib.sha256(json.dumps(snapshot_data, sort_keys=True).encode()).hexdigest()
        snapshot_data["snapshot_id"] = snapshot_id
        self.snapshots.append(snapshot_data)
        return snapshot_id

    def _get_current_state(self) -> Dict[str, Any]:
        state = {}
        for block in self.chain:
            for tx in block.get("transactions", []):
                sender = tx["sender"]
                recipient = tx["recipient"]
                amount = tx["amount"]
                state[sender] = state.get(sender, 0.0) - amount
                state[recipient] = state.get(recipient, 0.0) + amount
        return state

    def _get_pending_transactions(self) -> List[Dict[str, Any]]:
        return []

    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        for snap in self.snapshots:
            if snap["snapshot_id"] == snapshot_id:
                return snap
        return None

    def list_snapshots(self) -> List[Dict[str, str]]:
        return [{"id": s["snapshot_id"], "name": s["name"], "time": s["timestamp"]} for s in self.snapshots]
