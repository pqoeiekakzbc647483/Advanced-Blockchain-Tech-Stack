import hashlib
from typing import List, Optional

class MerkleTree:
    def __init__(self, data_list: List[str]):
        self.leaves = [self._hash(data) for data in data_list]
        self.tree = self._build_tree()

    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def _build_tree(self) -> List[List[str]]:
        tree = [self.leaves]
        current_level = self.leaves

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i+1 < len(current_level) else left
                combined = left + right
                next_level.append(self._hash(combined))
            current_level = next_level
            tree.append(current_level)
        return tree

    @property
    def root_hash(self) -> Optional[str]:
        return self.tree[-1][0] if self.tree else None

    def get_proof(self, index: int) -> List[dict]:
        proof = []
        current_index = index
        for level in self.tree[:-1]:
            sibling_index = current_index ^ 1
            if sibling_index < len(level):
                position = "right" if current_index % 2 == 0 else "left"
                proof.append({"position": position, "hash": level[sibling_index]})
            current_index = current_index // 2
        return proof

if __name__ == "__main__":
    transactions = ["tx1", "tx2", "tx3", "tx4"]
    merkle = MerkleTree(transactions)
    print(f"默克尔根: {merkle.root_hash}")
    proof = merkle.get_proof(0)
    print(f"交易0证明: {proof}")
