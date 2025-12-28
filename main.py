from tkinter import ttk

from src.buttons.on_create import on_create
from src.buttons.or_read import on_read
from src.create_db import create_db
import tkinter as tk

if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("600x350")
    root.resizable(False, False)

    # Основной контейнер
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True)

    # Заголовок
    title = ttk.Label(
        main_frame,
        text="Менеджер паролей",
        font=("Segoe UI", 14, "bold")
    )
    title.pack(pady=(0, 20))

    # Кнопки
    btn_create = ttk.Button(
        main_frame,
        text="Создать",
        command=on_create,
        width=20
    )
    btn_create.pack(pady=5)

    btn_read = ttk.Button(
        main_frame,
        text="Прочитать",
        command=on_read,
        width=20
    )
    btn_read.pack(pady=5)



    root.mainloop()
