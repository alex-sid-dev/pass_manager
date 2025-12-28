import sqlite3

from loguru import logger


def delete_passwords(id: int):
    conn = sqlite3.connect("passwords")
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
