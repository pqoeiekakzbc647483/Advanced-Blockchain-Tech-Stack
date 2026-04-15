import time
from typing import Dict

class YieldFarming:
    def __init__(self, reward_rate: float = 0.001):
        self.staked_positions: Dict[str, Dict] = {}
        self.reward_rate = reward_rate

    def stake(self, user: str, pool_id: str, amount: float) -> bool:
        if amount <= 0:
            return False
        
        key = f"{user}_{pool_id}"
        now = time.time()
        
        if key in self.staked_positions:
            self._update_rewards(key)
            self.staked_positions[key]["amount"] += amount
        else:
            self.staked_positions[key] = {
                "user": user,
                "pool_id": pool_id,
                "amount": amount,
                "rewards": 0.0,
                "last_update": now
            }
        return True

    def unstake(self, user: str, pool_id: str, amount: float) -> bool:
        key = f"{user}_{pool_id}"
        if key not in self.staked_positions:
            return False
        
        self._update_rewards(key)
        position = self.staked_positions[key]
        
        if position["amount"] < amount:
            return False
        
        position["amount"] -= amount
        if position["amount"] == 0:
            del self.staked_positions[key]
        return True

    def _update_rewards(self, key: str) -> None:
        position = self.staked_positions[key]
        now = time.time()
        elapsed = now - position["last_update"]
        new_rewards = position["amount"] * self.reward_rate * (elapsed / 86400)
        position["rewards"] += new_rewards
        position["last_update"] = now

    def claim_rewards(self, user: str, pool_id: str) -> float:
        key = f"{user}_{pool_id}"
        if key not in self.staked_positions:
            return 0.0
        
        self._update_rewards(key)
        rewards = self.staked_positions[key]["rewards"]
        self.staked_positions[key]["rewards"] = 0.0
        return rewards
