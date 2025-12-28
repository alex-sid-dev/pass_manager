from loguru import logger
import sqlite3

from typing import List

from src.models.passwords import PasswordForChange


def read_passwords(description: str) -> List[PasswordForChange]:
    conn = sqlite3.connect("passwords")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       SELECT id, login, password, description
                       FROM passwords
                       WHERE description LIKE ?
                       """, (f"%{description}%",))

        rows = cursor.fetchall()

        if not rows:
            logger.info(f"Пароли по описанию '{description}' не найдены.")
            return []

        passwords = [
            PasswordForChange(
                id=id,
                login=login,
                password=password,
                description=desc
            )
            for id, login, password, desc in rows
        ]

        logger.info(
            f"Найдено {len(passwords)} записей по описанию '{description}'"
        )
        return passwords

    finally:
        conn.close()
