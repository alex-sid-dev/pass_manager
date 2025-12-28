from tkinter import messagebox, Toplevel, ttk

from src.buttons.on_delete import delete_selected
from src.buttons.on_edit import edit_selected
from src.crypto import PasswordCipher
from src.models.passwords import PasswordForChange
from src.read_password import read_passwords


def on_read():
    win = Toplevel()
    win.title("Чтение паролей")
    win.geometry("600x350")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=15)
    frame.pack(expand=True, fill="both")

    # Поиск
    search_frame = ttk.Frame(frame)
    search_frame.pack(fill="x", pady=(0, 10))

    ttk.Label(search_frame, text="Описание:").pack(side="left")

    entry_desc = ttk.Entry(search_frame)
    entry_desc.pack(side="left", padx=5, fill="x", expand=True)

    # Таблица
    columns = ("id", "login", "password", "description")
    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=10,
        selectmode="extended"  # ← позволяет выбирать несколько строк
    )

    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(fill="x", pady=10)

    ttk.Button(
        buttons_frame,
        text="Изменить",
        command=lambda: edit_selected(tree)
    ).pack(side="left", padx=5)

    ttk.Button(
        buttons_frame,
        text="Удалить",
        command=lambda: delete_selected(tree)
    ).pack(side="left", padx=5)

    tree.heading("id", text="ID")
    tree.heading("login", text="Логин")
    tree.heading("password", text="Пароль")
    tree.heading("description", text="Описание")

    tree.column("id", width=150)
    tree.column("login", width=150)
    tree.column("password", width=150)
    tree.column("description", width=250)

    tree.pack(fill="both", expand=True)

    def search():
        desc = entry_desc.get().strip()
        cipher = PasswordCipher()

        # очистка таблицы
        for row in tree.get_children():
            tree.delete(row)

        try:
            passwords: list[PasswordForChange] = read_passwords(desc)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        if not passwords:
            messagebox.showinfo("Результат", "Ничего не найдено")
            return

        for pwd in passwords:
            tree.insert(
                "",
                "end",
                values=(pwd.id, pwd.login, cipher.decrypt(pwd.password), pwd.description)
            )

    ttk.Button(
        search_frame,
        text="Найти",
        command=search
    ).pack(side="left", padx=5)
