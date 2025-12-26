from utils.create_db import create_db
from utils.crypto import PasswordCipher

if __name__ == "__main__":
    create_db()
    cipher = PasswordCipher()

    encrypted_1 = cipher.encrypt("mypassword123")
    print("Зашифровано:", encrypted_1)