from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64

class TransactionEncryption:
    def __init__(self):
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)

    def generate_asymmetric_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt_transaction_symmetric(self, tx_data: str) -> str:
        encrypted = self.fernet.encrypt(tx_data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_transaction_symmetric(self, encrypted_data: str) -> str:
        decoded = base64.b64decode(encrypted_data)
        decrypted = self.fernet.decrypt(decoded)
        return decrypted.decode()

    def encrypt_with_public_key(self, public_key, data: str) -> str:
        encrypted = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode()

    def decrypt_with_private_key(self, private_key, encrypted_data: str) -> str:
        decoded = base64.b64decode(encrypted_data)
        decrypted = private_key.decrypt(
            decoded,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()
