import sqlite3
from pathlib import Path

from loguru import logger

BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "pass_manager":
    BASE_DIR = BASE_DIR.parent
passwords_file_dir = BASE_DIR / "passwords"


def delete_passwords(id: int):
    conn = sqlite3.connect(passwords_file_dir)
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM passwords
                       WHERE id = ?
                       """, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            logger.info(f"Запись с номером '{id}' не найдена.")
        else:
            logger.info(f"Пароль для '{id}' успешно удален.")
    finally:
        conn.close()
