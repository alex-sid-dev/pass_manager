from tkinter import Toplevel, ttk

from src.crypto import PasswordCipher
from src.models.passwords import PasswordForChange
from src.update_password import update_password


def open_edit_window(tree, id, item_id, login, password, description):
    win = Toplevel()
    win.title("Редактировать запись")
    win.geometry("600x350")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="id").pack(anchor="w")
    e_id = ttk.Entry(frame)
    e_id.insert(0, id)
    e_id.config(state="readonly")
    e_id.pack(fill="x", pady=5)

    ttk.Label(frame, text="Логин").pack(anchor="w")
    e_login = ttk.Entry(frame)
    e_login.insert(0, login)
    e_login.pack(fill="x", pady=5)

    ttk.Label(frame, text="Пароль").pack(anchor="w")
    e_pass = ttk.Entry(frame)
    e_pass.insert(0, password)
    e_pass.pack(fill="x", pady=5)

    ttk.Label(frame, text="Описание").pack(anchor="w")
    e_desc = ttk.Entry(frame)
    e_desc.insert(0, description)
    e_desc.pack(fill="x", pady=5)

    def save():
        cipher = PasswordCipher()
        new_pwd = PasswordForChange(
            id=int(e_id.get()),
            login=e_login.get().strip(),
            password=e_pass.get().strip(),
            description=e_desc.get().strip()
        )

        update_password(
            id=int(e_id.get()),
            new_login=e_login.get().strip(),
            new_password=new_pwd.password,
            new_description=e_desc.get().strip()
        )

        tree.item(
            item_id,
            values=(new_pwd.login, e_pass.get().strip(), new_pwd.description)
        )
        win.destroy()

    ttk.Button(frame, text="Сохранить", command=save).pack(pady=15)
