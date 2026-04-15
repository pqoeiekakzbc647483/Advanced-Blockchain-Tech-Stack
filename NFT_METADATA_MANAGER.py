import json
import hashlib
from datetime import datetime
from typing import Dict, Any

class NFTMetadataManager:
    def __init__(self):
        self.nft_registry: Dict[int, Dict[str, Any]] = {}
        self.token_counter = 1

    def create_nft_metadata(self, creator: str, name: str, description: str, image_url: str, attributes: list) -> tuple[int, str]:
        token_id = self.token_counter
        self.token_counter += 1

        metadata = {
            "token_id": token_id,
            "name": name,
            "description": description,
            "image": image_url,
            "attributes": attributes,
            "creator": creator,
            "mint_time": datetime.utcnow().isoformat(),
            "version": "1.0"
        }

        metadata_hash = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode()).hexdigest()
        self.nft_registry[token_id] = {
            "metadata": metadata,
            "hash": metadata_hash,
            "owner": creator
        }
        return token_id, metadata_hash

    def transfer_nft(self, token_id: int, new_owner: str) -> bool:
        if token_id not in self.nft_registry:
            return False
        self.nft_registry[token_id]["owner"] = new_owner
        return True

    def get_metadata(self, token_id: int) -> Dict[str, Any]:
        return self.nft_registry.get(token_id, {}).get("metadata", {})

if __name__ == "__main__":
    manager = NFTMetadataManager()
    tid, hsh = manager.create_nft_metadata(
        creator="user_wallet",
        name="Digital Art #1",
        description="Abstract blockchain art",
        image_url="ipfs://art_hash",
        attributes=[{"trait": "color", "value": "blue"}]
    )
