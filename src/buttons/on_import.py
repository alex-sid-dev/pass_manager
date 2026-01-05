from tkinter import Toplevel, Button

from src.buttons.on_import_csv import import_csv
from src.crypto_utils.crypto import PasswordCipher


def on_import(cipher: PasswordCipher):
    win = Toplevel()
    win.title("Импорт паролей")
    win.geometry("600x350")
    win.resizable(False, False)

    btn_import = Button(
        win,
        text="Выбрать CSV файл",
        width=25,
        height=2,
        command=lambda: import_csv(cipher)
    )

    btn_import.pack(expand=True)
