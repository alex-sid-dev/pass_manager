import sqlite3
from pathlib import Path

from loguru import logger

from src.models.passwords import Password

BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "pass_manager":
    BASE_DIR = BASE_DIR.parent
passwords_file_dir = BASE_DIR / "passwords"


def create_password(pwd: Password):
    conn = sqlite3.connect(passwords_file_dir)
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO passwords (login, password, description)
                       VALUES (?, ?, ?)
                       """, (pwd.login, pwd.password, pwd.description))
        conn.commit()
        logger.info(f"Пароль для {pwd.login} успешно создан.")
    except sqlite3.IntegrityError:
        logger.info(f"Ошибка: логин '{pwd.login}' уже существует.")
    finally:
        conn.close()
