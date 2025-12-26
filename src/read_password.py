from loguru import logger

import sqlite3


def read_password(description: str):
    conn = sqlite3.connect("passwords")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       SELECT password
                       FROM passwords
                       WHERE description = ?
                       """, (description,))
        result = cursor.fetchone()

        if result is not None:
            password = result[0]
            logger.info(f"Пароль для '{description}' успешно прочитан: {password}")
            return password
        else:
            logger.info(f"Пароль для '{description}' не найден.")
            return None
    finally:
        conn.close()
