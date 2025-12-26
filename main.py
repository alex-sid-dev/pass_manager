from src.create_db import create_db
from src.create_password import create_password
from src.crypto import PasswordCipher
from src.delete_password import delete_password
from src.read_password import read_password

if __name__ == "__main__":
    create_db()
    cipher = PasswordCipher()
    password = cipher.encrypt("password542")

    create_password(login="user", password=password, description="abc")
    password1 = read_password("abc")
    delete_password("abc")
    password2 = read_password("abc")

