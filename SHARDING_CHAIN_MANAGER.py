from typing import List, Dict, Any
from uuid import uuid4

class ShardManager:
    def __init__(self, total_shards: int = 4):
        self.total_shards = total_shards
        self.shards: Dict[str, List[Dict[str, Any]]] = {f"shard_{i}": [] for i in range(total_shards)}
        self.shard_validators: Dict[str, List[str]] = {f"shard_{i}": [] for i in range(total_shards)}

    def assign_address_to_shard(self, address: str) -> str:
        addr_hash = hash(address)
        shard_index = addr_hash % self.total_shards
        return f"shard_{shard_index}"

    def add_transaction_to_shard(self, tx: Dict[str, Any]) -> bool:
        shard_id = self.assign_address_to_shard(tx["sender"])
        tx["shard_id"] = shard_id
        tx["tx_id"] = str(uuid4())
        self.shards[shard_id].append(tx)
        return True

    def register_validator(self, shard_id: str, validator: str) -> bool:
        if shard_id not in self.shards:
            return False
        if validator not in self.shard_validators[shard_id]:
            self.shard_validators[shard_id].append(validator)
            return True
        return False

    def get_shard_transactions(self, shard_id: str) -> List[Dict[str, Any]]:
        return self.shards.get(shard_id, [])

    def get_shard_count(self) -> int:
        return self.total_shards
