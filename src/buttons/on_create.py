from tkinter import ttk, Toplevel, messagebox

from src.create_password import create_password
from src.crypto import PasswordCipher
from src.models.passwords import Password

def on_create():
    win = Toplevel()
    win.title("Создать пароль")
    win.geometry("600x350")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=15)
    frame.pack(expand=True, fill="both")

    # Поля
    ttk.Label(frame, text="Логин").pack(anchor="w")
    entry_login = ttk.Entry(frame)
    entry_login.pack(fill="x", pady=5)

    ttk.Label(frame, text="Пароль").pack(anchor="w")
    entry_password = ttk.Entry(frame, show="*")
    entry_password.pack(fill="x", pady=5)

    ttk.Label(frame, text="Описание").pack(anchor="w")
    entry_desc = ttk.Entry(frame)
    entry_desc.pack(fill="x", pady=5)

    def save():
        login = entry_login.get().strip()
        password = entry_password.get().strip()
        cipher = PasswordCipher()
        password_cipher = cipher.encrypt(password)
        desc = entry_desc.get().strip()

        if not login or not password:
            messagebox.showerror("Ошибка", "Логин и пароль обязательны")
            return

        pwd = Password(
            login=login,
            password=password_cipher,
            description=desc
        )

        create_password(pwd)
        messagebox.showinfo("Успех", "Пароль сохранён")
        win.destroy()

    ttk.Button(frame, text="Сохранить", command=save).pack(pady=15)
