from typing import List, Dict, Any
from collections import defaultdict

class ChainAnalytics:
    def __init__(self, blockchain: List[Dict[str, Any]]):
        self.chain = blockchain
        self.address_activity = defaultdict(lambda: {"sent": 0.0, "received": 0.0, "tx_count": 0})

    def calculate_total_transactions(self) -> int:
        count = 0
        for block in self.chain:
            count += len(block.get("transactions", []))
        return count

    def analyze_address_activity(self) -> Dict[str, Dict[str, float]]:
        for block in self.chain:
            for tx in block.get("transactions", []):
                sender = tx.get("sender")
                recipient = tx.get("recipient")
                amount = tx.get("amount", 0.0)
                
                self.address_activity[sender]["sent"] += amount
                self.address_activity[sender]["tx_count"] += 1
                self.address_activity[recipient]["received"] += amount
                self.address_activity[recipient]["tx_count"] += 1
        return dict(self.address_activity)

    def get_top_addresses(self, top_n: int = 5) -> List[tuple]:
        activity = self.analyze_address_activity()
        sorted_addresses = sorted(activity.items(), key=lambda x: x[1]["tx_count"], reverse=True)
        return sorted_addresses[:top_n]

    def calculate_block_time_avg(self) -> float:
        if len(self.chain) <= 1:
            return 0.0
        
        total_diff = 0.0
        for i in range(1, len(self.chain)):
            total_diff += self.chain[i]["timestamp"] - self.chain[i-1]["timestamp"]
        return total_diff / (len(self.chain) - 1)
