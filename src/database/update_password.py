import sqlite3
from pathlib import Path
from tkinter import messagebox

from loguru import logger

from src.crypto_utils.crypto import PasswordCipher

BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "pass_manager":
    BASE_DIR = BASE_DIR.parent
passwords_file_dir = BASE_DIR / "passwords"


def update_password(id: int, new_login: str, new_description: str, new_password: str, cipher: PasswordCipher):
    conn = sqlite3.connect(passwords_file_dir)
    cursor = conn.cursor()
    if new_login is None and new_password is None and new_description is None:
        messagebox.showinfo("Обновление", "Нет данных для обновления")
        return

    try:
        # формируем SET часть запроса динамически
        updates = []
        params = []

        if new_login is not None:
            updates.append("login = ?")
            params.append(new_login)
        if new_password is not None:
            updates.append("password = ?")
            decrypt_pass = cipher.encrypt(new_password)
            params.append(decrypt_pass)
        if new_description is not None:
            updates.append("description = ?")
            params.append(new_description)

        params.append(id)
        logger.info(f"айди: {id}, login: {new_login}, password: {new_password}, description: {new_description}")

        sql = f"UPDATE passwords SET {', '.join(updates)} WHERE id = ?"
        logger.info(sql)
        cursor.execute(sql, params)
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Обновление", "Запись с таким ID не найдена")
        else:
            messagebox.showinfo("Обновление", "Пароль успешно обновлён")

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка БД", str(e))
    finally:
        conn.close()
