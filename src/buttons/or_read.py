import threading
from tkinter import messagebox, Toplevel, ttk

from src.buttons.on_delete import delete_selected
from src.buttons.on_edit import edit_selected
from src.crypto_utils.crypto import PasswordCipher
from src.database.read_password import read_passwords
from src.models.passwords import PasswordForChange


def on_read(cipher: PasswordCipher):
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
    entry_desc.focus_set()

    # биндим Enter на поле
    entry_desc.bind("<Return>", lambda event: search())

    ttk.Button(search_frame, text="Найти", width=10, command=lambda: search()).pack(side="left", padx=5)

    # Таблица
    columns = ("id", "login", "password", "description")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10, selectmode="extended")

    # Кнопки действий
    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(fill="x", pady=10)

    ttk.Button(buttons_frame, text="Изменить", command=lambda: edit_selected(tree, cipher)).pack(side="left", padx=5)
    ttk.Button(buttons_frame, text="Удалить", command=lambda: delete_selected(tree)).pack(side="left", padx=5)

    # Настройка колонок
    tree.heading("id", text="ID")
    tree.heading("login", text="Логин")
    tree.heading("password", text="Пароль")
    tree.heading("description", text="Описание")

    tree.column("id", width=40)
    tree.column("login", width=150)
    tree.column("password", width=150)
    tree.column("description", width=250)

    tree.pack(fill="both", expand=True)

    # --- Функция поиска ---
    def search():
        desc = entry_desc.get().strip()

        # Очистка таблицы
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

    # --- Функция копирования по двойному клику ---
    def copy_cell(event):
        selected_item = tree.identify_row(event.y)
        if not selected_item:
            return

        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        col = tree.identify_column(event.x)
        value = tree.item(selected_item, "values")[int(col[1:]) - 1]
        win.clipboard_clear()
        win.clipboard_append(value)

        # Тултип-подсказка
        tooltip = ttk.Label(win, text=f"Скопировано: {value}", background="red")
        tooltip.place(relx=0.5, rely=0, anchor="n")

        # Скрываем через 1.5 секунды
        def hide_tooltip():
            tooltip.destroy()

        threading.Timer(1.5, hide_tooltip).start()

        tree.focus_set()  # возвращаем фокус

    tree.bind("<Double-1>", copy_cell)
