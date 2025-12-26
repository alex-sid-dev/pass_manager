from cryptography.fernet import Fernet
import os

class PasswordCipher:
    def __init__(self, key_file="secret.key"):
        self.key_file = key_file
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def encrypt(self, password: str) -> str:
        encrypted = self.cipher.encrypt(password.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_password: str) -> str:
        decrypted = self.cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()

