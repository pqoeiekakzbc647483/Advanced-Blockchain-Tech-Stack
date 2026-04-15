import random
from typing import Dict, List

class PoSConsensus:
    def __init__(self, min_stake: float = 100.0):
        self.stakers: Dict[str, float] = {}
        self.min_stake = min_stake
        self.current_validator = None

    def stake_tokens(self, address: str, amount: float) -> bool:
        if amount <= 0:
            return False
        self.stakers[address] = self.stakers.get(address, 0.0) + amount
        return True

    def unstake_tokens(self, address: str, amount: float) -> bool:
        if self.stakers.get(address, 0.0) < amount:
            return False
        self.stakers[address] -= amount
        if self.stakers[address] == 0:
            del self.stakers[address]
        return True

    def select_validator(self) -> str:
        eligible = [addr for addr, stake in self.stakers.items() if stake >= self.min_stake]
        if not eligible:
            raise ValueError("No eligible validators")
        
        total_stake = sum(self.stakers[addr] for addr in eligible)
        selection = random.uniform(0, total_stake)
        current = 0.0
        
        for addr in eligible:
            current += self.stakers[addr]
            if current >= selection:
                self.current_validator = addr
                return addr
        return eligible[-1]

    def get_validator_list(self) -> List[str]:
        return [addr for addr, stake in self.stakers.items() if stake >= self.min_stake]
