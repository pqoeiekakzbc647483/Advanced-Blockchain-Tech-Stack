import time
from typing import Dict, Optional

class TokenVesting:
    def __init__(self):
        self.vesting_plans: Dict[str, Dict] = {}

    def create_vesting_plan(self, beneficiary: str, total_amount: float, start_time: float, duration: int, cliff: int = 0) -> bool:
        if beneficiary in self.vesting_plans:
            return False
        
        self.vesting_plans[beneficiary] = {
            "total": total_amount,
            "released": 0.0,
            "start": start_time,
            "cliff": start_time + cliff,
            "end": start_time + duration,
            "duration": duration
        }
        return True

    def get_releasable_amount(self, beneficiary: str) -> float:
        plan = self.vesting_plans.get(beneficiary)
        if not plan:
            return 0.0
        
        now = time.time()
        if now < plan["cliff"]:
            return 0.0
        
        if now >= plan["end"]:
            return plan["total"] - plan["released"]
        
        elapsed = now - plan["start"]
        vested = plan["total"] * (elapsed / plan["duration"])
        return vested - plan["released"]

    def release_tokens(self, beneficiary: str) -> float:
        amount = self.get_releasable_amount(beneficiary)
        if amount <= 0:
            return 0.0
        
        self.vesting_plans[beneficiary]["released"] += amount
        return amount

    def get_plan(self, beneficiary: str) -> Optional[Dict]:
        return self.vesting_plans.get(beneficiary)
