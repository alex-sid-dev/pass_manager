import sqlite3
from pathlib import Path
from typing import List

from loguru import logger

from src.models.passwords import PasswordForChange

BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "pass_manager":
    BASE_DIR = BASE_DIR.parent
passwords_file_dir = BASE_DIR / "passwords"


def read_passwords(description: str) -> List[PasswordForChange]:
    conn = sqlite3.connect(passwords_file_dir)
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

def get_all_passwords():
    conn = sqlite3.connect(passwords_file_dir)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT login, password, description
        FROM passwords
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
