import requests
import time
import hashlib
from typing import Optional, Dict, Any

class BlockchainOracle:
    def __init__(self, oracle_id: str):
        self.oracle_id = oracle_id
        self.data_cache: Dict[str, Dict[str, Any]] = {}

    def fetch_price_data(self, token_symbol: str) -> Optional[float]:
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_symbol}&vs_currencies=usd"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()[token_symbol]["usd"]
        except Exception:
            return None
        return None

    def format_data_for_chain(self, data: Any, data_type: str) -> Dict[str, Any]:
        timestamp = time.time()
        data_hash = hashlib.sha256(str(data).encode()).hexdigest()
        return {
            "oracle_id": self.oracle_id,
            "data_type": data_type,
            "data": data,
            "timestamp": timestamp,
            "data_hash": data_hash
        }

    def request_external_data(self, data_type: str, query: str) -> Optional[Dict[str, Any]]:
        if data_type == "price":
            data = self.fetch_price_data(query)
            if data:
                formatted = self.format_data_for_chain(data, data_type)
                self.data_cache[query] = formatted
                return formatted
        return None

    def get_cached_data(self, query: str) -> Optional[Dict[str, Any]]:
        return self.data_cache.get(query)
