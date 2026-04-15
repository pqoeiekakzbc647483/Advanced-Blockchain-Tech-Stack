from typing import List, Dict, Any
import hashlib

class ForkDetector:
    def __init__(self, fork_threshold: int = 2):
        self.fork_threshold = fork_threshold

    def compare_chains(self, local_chain: List[Dict[str, Any]], remote_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        common_prefix = self._find_common_prefix(local_chain, remote_chain)
        local_fork_length = len(local_chain) - common_prefix
        remote_fork_length = len(remote_chain) - common_prefix

        return {
            "common_block_index": common_prefix - 1,
            "local_fork_length": local_fork_length,
            "remote_fork_length": remote_fork_length,
            "fork_detected": local_fork_length >= self.fork_threshold or remote_fork_length >= self.fork_threshold,
            "recommended_chain": "remote" if remote_fork_length > local_fork_length else "local"
        }

    def _find_common_prefix(self, chain_a: List[Dict[str, Any]], chain_b: List[Dict[str, Any]]) -> int:
        min_length = min(len(chain_a), len(chain_b))
        for i in range(min_length):
            if self._hash_block(chain_a[i]) != self._hash_block(chain_b[i]):
                return i
        return min_length

    @staticmethod
    def _hash_block(block: Dict[str, Any]) -> str:
        block_copy = block.copy()
        block_copy.pop("hash", None)
        return hashlib.sha256(str(block_copy).encode()).hexdigest()

    def is_chain_valid(self, chain: List[Dict[str, Any]]) -> bool:
        return len(chain) > 0
