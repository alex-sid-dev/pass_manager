import tkinter as tk
from tkinter import ttk, messagebox

from src.buttons.on_create import on_create
from src.buttons.on_export import on_export
from src.buttons.on_import import on_import
from src.buttons.or_read import on_read
from src.crypto_utils.crypto import PasswordCipher
from src.crypto_utils.hash_password import hash_password
from src.database.create_db import create_db, get_master_hash, set_master_hash, create_master_db


def open_main_window(cipher: PasswordCipher):
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("600x350")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True)

    title = ttk.Label(main_frame, text="Менеджер паролей", font=("Segoe UI", 14, "bold"))
    title.pack(pady=(0, 20))

    ttk.Button(main_frame, text="Создать", command=lambda: on_create(cipher), width=20).pack(pady=5)
    ttk.Button(main_frame, text="Прочитать", command=lambda: on_read(cipher), width=20).pack(pady=5)
    ttk.Button(main_frame, text="Импортировать", command=lambda: on_import(cipher), width=20).pack(pady=5)
    ttk.Button(main_frame, text="Экспортировать", command=lambda: on_export(cipher), width=20).pack(pady=5)

    root.mainloop()


def ask_for_password(stored_hash):
    def check_password():
        entered = entry.get()
        if hash_password(entered) == stored_hash:
            login_window.destroy()
            cipher = PasswordCipher(entered)
            open_main_window(cipher)

        else:
            messagebox.showerror("Ошибка", "Неверный пароль")
            entry.delete(0, tk.END)

    login_window = tk.Tk()
    login_window.title("Вход")
    login_window.geometry("400x150")
    login_window.resizable(False, False)

    ttk.Label(login_window, text="Введите мастер-пароль:", font=("Segoe UI", 12)).pack(pady=10)
    entry = ttk.Entry(login_window, show="*")
    entry.pack(pady=5)
    entry.focus()

    entry.bind("<Return>", lambda event: check_password())

    ttk.Button(login_window, text="Войти", command=check_password).pack(pady=10)

    login_window.mainloop()


def create_new_password():
    def save_password():
        pwd = entry.get()
        if len(pwd) < 4:
            messagebox.showwarning("Ошибка", "Пароль слишком короткий!")
            return
        set_master_hash(hash_password(pwd))
        messagebox.showinfo("Готово", "Мастер-пароль сохранен")
        create_window.destroy()
        cipher = PasswordCipher(pwd)
        open_main_window(cipher)

    create_window = tk.Tk()
    create_window.title("Создать мастер-пароль")
    create_window.geometry("600x150")
    create_window.resizable(False, False)

    ttk.Label(create_window, text="Введите новый мастер-пароль:", font=("Segoe UI", 12)).pack(pady=10)
    entry = ttk.Entry(create_window, show="*")
    entry.pack(pady=5)
    entry.focus()
    ttk.Button(create_window, text="Сохранить", command=save_password).pack(pady=10)

    create_window.mainloop()


# --- Главная логика ---
if __name__ == "__main__":
    create_db()
    create_master_db()
    master_hash = get_master_hash()

    if master_hash:
        ask_for_password(master_hash)
    else:
        create_new_password()
