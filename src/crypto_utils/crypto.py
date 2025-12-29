import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "pass_manager":
    BASE_DIR = BASE_DIR.parent
salt_file_dir = BASE_DIR / "salt.bin"


class PasswordCipher:
    def __init__(self, master_password: str, salt_file=salt_file_dir):
        self.salt_file = salt_file
        self.salt = self._load_or_create_salt()
        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)

    def _load_or_create_salt(self):
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "rb") as f:
                return f.read()
        else:
            salt = os.urandom(16)  # 16 байт для PBKDF2
            with open(self.salt_file, "wb") as f:
                f.write(salt)
            return salt

    def _derive_key(self, password: str) -> bytes:
        # PBKDF2HMAC превращает пароль в 32-байтовый ключ
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt(self, password: str) -> str:
        encrypted = self.cipher.encrypt(password.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_password: str) -> str:
        decrypted = self.cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()
