from typing import Dict, List

class TokenSwapRouter:
    def __init__(self):
        self.pools: Dict[str, Dict] = {}

    def add_pool(self, pool_id: str, token_a: str, token_b: str, reserve_a: float, reserve_b: float) -> None:
        self.pools[pool_id] = {
            "token_a": token_a,
            "token_b": token_b,
            "reserve_a": reserve_a,
            "reserve_b": reserve_b,
            "fee": 0.003
        }

    def get_pool_for_pair(self, token_in: str, token_out: str) -> str:
        for pid, pool in self.pools.items():
            if (pool["token_a"] == token_in and pool["token_b"] == token_out) or \
               (pool["token_a"] == token_out and pool["token_b"] == token_in):
                return pid
        return ""

    def calculate_swap_output(self, pool_id: str, token_in: str, amount_in: float) -> float:
        pool = self.pools.get(pool_id)
        if not pool:
            return 0.0

        fee = amount_in * pool["fee"]
        amount_in_after_fee = amount_in - fee

        if pool["token_a"] == token_in:
            new_reserve_a = pool["reserve_a"] + amount_in_after_fee
            new_reserve_b = (pool["reserve_a"] * pool["reserve_b"]) / new_reserve_a
            return pool["reserve_b"] - new_reserve_b
        else:
            new_reserve_b = pool["reserve_b"] + amount_in_after_fee
            new_reserve_a = (pool["reserve_a"] * pool["reserve_b"]) / new_reserve_b
            return pool["reserve_a"] - new_reserve_a

    def swap(self, pool_id: str, token_in: str, amount_in: float) -> float:
        output = self.calculate_swap_output(pool_id, token_in, amount_in)
        if output <= 0:
            return 0.0

        pool = self.pools[pool_id]
        if pool["token_a"] == token_in:
            pool["reserve_a"] += amount_in * 0.997
            pool["reserve_b"] -= output
        else:
            pool["reserve_b"] += amount_in * 0.997
            pool["reserve_a"] -= output
        return output
