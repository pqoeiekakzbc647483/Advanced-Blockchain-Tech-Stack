import time
from typing import List, Dict, Any
from heapq import heappush, heappop

class TransactionPool:
    def __init__(self, max_pool_size: int = 1000):
        self.pending_transactions: List[Dict[str, Any]] = []
        self.max_size = max_pool_size
        self.tx_ids = set()

    def add_transaction(self, tx_id: str, sender: str, recipient: str, amount: float, gas_fee: float) -> bool:
        if tx_id in self.tx_ids or len(self.pending_transactions) >= self.max_size:
            return False
        
        tx = {
            "tx_id": tx_id,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "gas_fee": gas_fee,
            "timestamp": time.time()
        }
        
        heappush(self.pending_transactions, (-gas_fee, tx))
        self.tx_ids.add(tx_id)
        return True

    def get_top_transactions(self, count: int) -> List[Dict[str, Any]]:
        result = []
        temp = []
        for _ in range(min(count, len(self.pending_transactions))):
            item = heappop(self.pending_transactions)
            result.append(item[1])
            temp.append(item)
        
        for item in temp:
            heappush(self.pending_transactions, item)
        return result

    def remove_transactions(self, tx_ids: List[str]) -> None:
        new_pool = []
        new_ids = set()
        for item in self.pending_transactions:
            tx = item[1]
            if tx["tx_id"] not in tx_ids:
                new_pool.append(item)
                new_ids.add(tx["tx_id"])
        
        self.pending_transactions = new_pool
        self.tx_ids = new_ids

    def pool_size(self) -> int:
        return len(self.pending_transactions)
