import hashlib
import time
from multiprocessing import Pool

class OptimizedPoW:
    def __init__(self, difficulty: int = 5):
        self.difficulty = difficulty
        self.prefix = "0" * self.difficulty

    def calculate_hash(self, data: str, nonce: int) -> str:
        value = f"{data}{nonce}".encode()
        return hashlib.sha256(value).hexdigest()

    def find_nonce_single(self, data: str) -> int:
        nonce = 0
        while True:
            hash_result = self.calculate_hash(data, nonce)
            if hash_result.startswith(self.prefix):
                return nonce
            nonce += 1

    def batch_mine(self, data_list: list) -> list:
        with Pool(processes=4) as pool:
            results = pool.map(self.find_nonce_single, data_list)
        return results

if __name__ == "__main__":
    pow = OptimizedPoW(difficulty=4)
    start = time.time()
    nonce = pow.find_nonce_single("block_data_1001")
    end = time.time()
    print(f"找到Nonce: {nonce}, 耗时: {end-start:.2f}s")
