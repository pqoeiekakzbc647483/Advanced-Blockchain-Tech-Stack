import hashlib
import json
from typing import Dict, Any, List

class BlockValidationEngine:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.required_prefix = "0" * difficulty

    def validate_single_block(self, block: Dict[str, Any], previous_block: Dict[str, Any]) -> bool:
        if not self._validate_block_hash(block):
            return False
        if block["previous_hash"] != self._hash(previous_block):
            return False
        if not self._validate_proof(block["proof"], previous_block["proof"]):
            return False
        if block["index"] != previous_block["index"] + 1:
            return False
        return True

    def validate_chain(self, chain: List[Dict[str, Any]]) -> bool:
        if len(chain) == 0:
            return True
        
        previous_block = chain[0]
        for block in chain[1:]:
            if not self.validate_single_block(block, previous_block):
                return False
            previous_block = block
        return True

    def _validate_proof(self, proof: int, last_proof: int) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith(self.required_prefix)

    def _validate_block_hash(self, block: Dict[str, Any]) -> bool:
        computed_hash = self._hash(block)
        return computed_hash == block.get("hash", computed_hash)

    @staticmethod
    def _hash(block: Dict[str, Any]) -> str:
        block_copy = block.copy()
        block_copy.pop("hash", None)
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
