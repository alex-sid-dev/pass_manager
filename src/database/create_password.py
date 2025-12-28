import sqlite3
from loguru import logger

from src.models.passwords import Password


def create_password(pwd: Password):
    conn = sqlite3.connect("passwords")
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


