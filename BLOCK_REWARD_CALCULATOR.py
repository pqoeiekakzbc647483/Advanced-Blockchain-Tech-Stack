class BlockRewardCalculator:
    def __init__(self, initial_reward: float = 10.0, halving_interval: int = 210000):
        self.initial_reward = initial_reward
        self.halving_interval = halving_interval

    def calculate_reward(self, block_height: int) -> float:
        halving_count = block_height // self.halving_interval
        reward = self.initial_reward / (2 ** halving_count)
        return max(reward, 0.0001)

    def calculate_total_mined(self, current_height: int) -> float:
        total = 0.0
        halving_count = current_height // self.halving_interval

        for i in range(halving_count):
            start = i * self.halving_interval
            end = (i + 1) * self.halving_interval
            if end > current_height:
                end = current_height
            reward = self.initial_reward / (2 ** i)
            total += (end - start) * reward

        return total

    def get_halving_info(self, block_height: int) -> dict:
        next_halving = ((block_height // self.halving_interval) + 1) * self.halving_interval
        current_reward = self.calculate_reward(block_height)
        next_reward = current_reward / 2

        return {
            "current_reward": current_reward,
            "next_halving_height": next_halving,
            "next_reward": next_reward,
            "blocks_until_halving": next_halving - block_height
        }
