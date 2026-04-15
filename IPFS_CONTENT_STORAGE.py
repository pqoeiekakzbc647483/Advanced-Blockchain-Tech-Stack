import hashlib
import json
from typing import Optional, Dict, Any

class IPFSSimulator:
    def __init__(self):
        self.storage: Dict[str, Dict[str, Any]] = {}

    def calculate_cid(self, content: str) -> str:
        content_bytes = content.encode()
        sha256_hash = hashlib.sha256(content_bytes).digest()
        cid = f"Qm{hashlib.sha256(sha256_hash).hexdigest()[:44]}"
        return cid

    def upload_content(self, content: str, content_type: str = "text/plain") -> str:
        cid = self.calculate_cid(content)
        self.storage[cid] = {
            "content": content,
            "type": content_type,
            "size": len(content.encode()),
            "timestamp": self._get_timestamp()
        }
        return cid

    def get_content(self, cid: str) -> Optional[str]:
        return self.storage.get(cid, {}).get("content")

    def get_metadata(self, cid: str) -> Optional[Dict[str, Any]]:
        return self.storage.get(cid)

    @staticmethod
    def _get_timestamp() -> float:
        import time
        return time.time()

if __name__ == "__main__":
    ipfs = IPFSSimulator()
    data = json.dumps({"nft_id": 100, "owner": "0x123"})
    cid = ipfs.upload_content(data, "application/json")
    content = ipfs.get_content(cid)
