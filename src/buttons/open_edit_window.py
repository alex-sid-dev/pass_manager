from tkinter import Toplevel, ttk, END

from src.database.update_password import update_password
from src.models.passwords import PasswordForChange
from src.utils import generate_password


def open_edit_window(tree, id, item_id, login, password, description, cipher):
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

    pass_frame = ttk.Frame(frame)
    pass_frame.pack(fill="x", pady=5)

    e_pass = ttk.Entry(pass_frame)
    e_pass.insert(0, password)
    e_pass.pack(side="left", fill="x", expand=True)

    def on_generate():
        new_password = generate_password(12)
        e_pass.delete(0, END)
        e_pass.insert(0, new_password)

    ttk.Button(
        pass_frame,
        text="Сгенерировать",
        command=on_generate
    ).pack(side="right", padx=5)

    ttk.Label(frame, text="Описание").pack(anchor="w")
    e_desc = ttk.Entry(frame)
    e_desc.insert(0, description)
    e_desc.pack(fill="x", pady=5)

    def save():
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
            new_description=e_desc.get().strip(),
            cipher=cipher
        )

        tree.item(
            item_id,
            values=(new_pwd.login, e_pass.get().strip(), new_pwd.description)
        )
        win.destroy()

    ttk.Button(frame, text="Сохранить", command=save).pack(pady=15)
