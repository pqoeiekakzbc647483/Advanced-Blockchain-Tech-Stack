import hashlib
import secrets
from cryptography.fernet import Fernet
from typing import Optional

class WalletKeyManager:
    def __init__(self):
        self.encrypted_keys = {}

    def generate_private_key(self) -> str:
        random_bytes = secrets.token_bytes(32)
        private_key = hashlib.sha256(random_bytes).hexdigest()
        return private_key

    def generate_public_address(self, private_key: str) -> str:
        key_hash = hashlib.sha256(private_key.encode()).digest()
        public_address = hashlib.ripemd160(key_hash).hexdigest()
        return f"0x{public_address}"

    def encrypt_key(self, private_key: str, password: str) -> str:
        key = hashlib.sha256(password.encode()).digest()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(private_key.encode())
        return encrypted.decode()

    def decrypt_key(self, encrypted_key: str, password: str) -> Optional[str]:
        try:
            key = hashlib.sha256(password.encode()).digest()
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted_key.encode())
            return decrypted.decode()
        except Exception:
            return None

    def create_wallet(self, password: str) -> dict:
        priv_key = self.generate_private_key()
        pub_addr = self.generate_public_address(priv_key)
        encrypted_priv = self.encrypt_key(priv_key, password)
        return {
            "public_address": pub_addr,
            "encrypted_private_key": encrypted_priv
        }

if __name__ == "__main__":
    wm = WalletKeyManager()
    wallet = wm.create_wallet("secure_password_123")
