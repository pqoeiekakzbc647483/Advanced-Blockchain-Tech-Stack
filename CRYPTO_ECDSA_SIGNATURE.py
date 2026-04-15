import ecdsa
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class ECDSASignatureTool:
    def __init__(self):
        self.curve = SECP256k1

    def generate_key_pair(self) -> tuple[SigningKey, VerifyingKey]:
        private_key = SigningKey.generate(curve=self.curve)
        public_key = private_key.get_verifying_key()
        return private_key, public_key

    def sign_message(self, private_key: SigningKey, message: str) -> bytes:
        message_hash = hashlib.sha256(message.encode()).digest()
        signature = private_key.sign(message_hash)
        return signature

    def verify_signature(self, public_key: VerifyingKey, signature: bytes, message: str) -> bool:
        try:
            message_hash = hashlib.sha256(message.encode()).digest()
            return public_key.verify(signature, message_hash)
        except ecdsa.BadSignatureError:
            return False

if __name__ == "__main__":
    tool = ECDSASignatureTool()
    priv_key, pub_key = tool.generate_key_pair()
    msg = "blockchain_transaction_001"
    sig = tool.sign_message(priv_key, msg)
    result = tool.verify_signature(pub_key, sig, msg)
    print(f"签名验证结果: {result}")
