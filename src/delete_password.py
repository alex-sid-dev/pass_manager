import sqlite3

from loguru import logger


def delete_password(description: str):
    conn = sqlite3.connect("passwords")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM passwords
                       WHERE description = ?
                       """, (description,))
        conn.commit()

        if cursor.rowcount == 0:
            logger.info(f"Запись с описанием '{description}' не найдена.")
        else:
            logger.info(f"Пароль для '{description}' успешно удален.")
    finally:
        conn.close()
