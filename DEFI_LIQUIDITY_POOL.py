class DefiLiquidityPool:
    def __init__(self):
        self.token_a_reserve = 0.0
        self.token_b_reserve = 0.0
        self.liquidity_providers = {}
        self.fee_rate = 0.003

    def add_liquidity(self, user: str, amount_a: float, amount_b: float) -> None:
        if self.token_a_reserve == 0 and self.token_b_reserve == 0:
            lp_tokens = (amount_a * amount_b) ** 0.5
        else:
            lp_tokens = min(
                amount_a * self.liquidity_total / self.token_a_reserve,
                amount_b * self.liquidity_total / self.token_b_reserve
            )
        
        self.token_a_reserve += amount_a
        self.token_b_reserve += amount_b
        self.liquidity_providers[user] = self.liquidity_providers.get(user, 0) + lp_tokens

    def remove_liquidity(self, user: str, lp_tokens: float) -> tuple[float, float]:
        total = self.liquidity_total
        if lp_tokens > self.liquidity_providers.get(user, 0):
            raise ValueError("Insufficient LP tokens")
        
        amount_a = lp_tokens * self.token_a_reserve / total
        amount_b = lp_tokens * self.token_b_reserve / total
        
        self.token_a_reserve -= amount_a
        self.token_b_reserve -= amount_b
        self.liquidity_providers[user] -= lp_tokens
        return amount_a, amount_b

    def swap_a_to_b(self, amount_a_in: float) -> float:
        fee = amount_a_in * self.fee_rate
        amount_in_after_fee = amount_a_in - fee
        new_a = self.token_a_reserve + amount_in_after_fee
        new_b = (self.token_a_reserve * self.token_b_reserve) / new_a
        amount_b_out = self.token_b_reserve - new_b
        
        self.token_a_reserve = new_a
        self.token_b_reserve = new_b
        return amount_b_out

    @property
    def liquidity_total(self) -> float:
        return sum(self.liquidity_providers.values())
