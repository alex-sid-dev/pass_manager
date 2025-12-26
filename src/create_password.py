import sqlite3
from loguru import logger


def create_password(login: str, password: str, description: str):
    conn = sqlite3.connect("passwords")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO passwords (login, password, description)
            VALUES (?, ?, ?)
        """, (login, password, description))
        conn.commit()
        logger.info(f"Пароль для {login} успешно создан.")
    except sqlite3.IntegrityError:
        logger.info(f"Ошибка: логин '{login}' уже существует.")
    finally:
        conn.close()


