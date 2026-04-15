import hashlib
import time
from typing import List, Dict

class MultiSigWallet:
    def __init__(self, owners: List[str], required_confirmations: int):
        self.owners = set(owners)
        self.required = required_confirmations
        self.transactions: Dict[str, Dict] = {}

    def is_owner(self, address: str) -> bool:
        return address in self.owners

    def submit_transaction(self, sender: str, to: str, value: float) -> str:
        if not self.is_owner(sender):
            raise ValueError("Not an owner")
        
        tx_id = hashlib.sha256(f"{sender}{to}{value}{time()}".encode()).hexdigest()
        self.transactions[tx_id] = {
            "to": to,
            "value": value,
            "confirmations": set(),
            "executed": False
        }
        return tx_id

    def confirm_transaction(self, owner: str, tx_id: str) -> bool:
        if tx_id not in self.transactions or not self.is_owner(owner):
            return False
        
        tx = self.transactions[tx_id]
        if tx["executed"]:
            return False
        
        tx["confirmations"].add(owner)
        return True

    def execute_transaction(self, tx_id: str) -> bool:
        if tx_id not in self.transactions:
            return False
        
        tx = self.transactions[tx_id]
        if len(tx["confirmations"]) >= self.required and not tx["executed"]:
            tx["executed"] = True
            return True
        return False

    def get_transaction(self, tx_id: str) -> Dict:
        return self.transactions.get(tx_id, {})
