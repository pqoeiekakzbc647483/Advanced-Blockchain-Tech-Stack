import time
from typing import Dict, Optional

class NFTMarketplace:
    def __init__(self):
        self.listings: Dict[str, Dict] = {}
        self.trades: Dict[str, Dict] = {}

    def list_nft(self, nft_id: str, seller: str, price: float) -> bool:
        if nft_id in self.listings:
            return False
        if price <= 0:
            return False
        
        self.listings[nft_id] = {
            "seller": seller,
            "price": price,
            "listed_at": time.time(),
            "active": True
        }
        return True

    def delist_nft(self, nft_id: str, seller: str) -> bool:
        if nft_id not in self.listings:
            return False
        if self.listings[nft_id]["seller"] != seller:
            return False
        
        self.listings[nft_id]["active"] = False
        return True

    def buy_nft(self, nft_id: str, buyer: str) -> Optional[Dict]:
        if nft_id not in self.listings:
            return None
        
        listing = self.listings[nft_id]
        if not listing["active"]:
            return None
        
        trade_id = f"trade_{nft_id}_{int(time.time())}"
        trade = {
            "trade_id": trade_id,
            "nft_id": nft_id,
            "seller": listing["seller"],
            "buyer": buyer,
            "price": listing["price"],
            "timestamp": time.time()
        }
        
        self.trades[trade_id] = trade
        listing["active"] = False
        return trade

    def get_listing(self, nft_id: str) -> Optional[Dict]:
        return self.listings.get(nft_id)

    def get_trade(self, trade_id: str) -> Optional[Dict]:
        return self.trades.get(trade_id)
