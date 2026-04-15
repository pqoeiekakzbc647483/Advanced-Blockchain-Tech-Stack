import hashlib
import json
from time import time
from typing import List, Dict, Any

class BlockchainCore:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = {
            "index": 0,
            "timestamp": time(),
            "transactions": [],
            "proof": 100,
            "previous_hash": "0",
        }
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "tx_time": time()
        })
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def mine_block(self) -> Dict[str, Any]:
        last_block = self.last_block
        proof = self.proof_of_work(last_block["proof"])
        previous_hash = self.hash(last_block)

        block = {
            "index": len(self.chain),
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash,
        }

        self.pending_transactions = []
        self.chain.append(block)
        return block

if __name__ == "__main__":
    chain = BlockchainCore()
    chain.add_transaction("wallet_1", "wallet_2", 5.0)
    chain.mine_block()
