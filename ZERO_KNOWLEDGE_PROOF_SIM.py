import hashlib
import random
from typing import Tuple

class ZKPSimulator:
    def __init__(self, secret: int):
        self.secret = secret
        self.public_modulus = 101
        self.public_base = 3

    def prover_commit(self) -> Tuple[int, int]:
        random_value = random.randint(1, 100)
        commitment = pow(self.public_base, random_value, self.public_modulus)
        return random_value, commitment

    def verifier_challenge(self) -> int:
        return random.randint(0, 1)

    def prover_response(self, random_val: int, challenge: int) -> int:
        response = (random_val + challenge * self.secret) % (self.public_modulus - 1)
        return response

    def verify(self, commitment: int, challenge: int, response: int) -> bool:
        left = pow(self.public_base, response, self.public_modulus)
        right = (commitment * pow(self.public_base, challenge * self.secret, self.public_modulus)) % self.public_modulus
        return left == right

if __name__ == "__main__":
    zkp = ZKPSimulator(secret=42)
    r, cmt = zkp.prover_commit()
    chal = zkp.verifier_challenge()
    resp = zkp.prover_response(r, chal)
    result = zkp.verify(cmt, chal, resp)
    print(f"零知识证明验证结果: {result}")
