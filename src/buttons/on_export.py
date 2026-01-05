from tkinter import Toplevel, Button

from src.buttons.on_export_csv import export_csv
from src.crypto_utils.crypto import PasswordCipher


def on_export(cipher: PasswordCipher):
    win = Toplevel()
    win.title("Экспорт паролей")
    win.geometry("600x350")
    win.resizable(False, False)

    btn_export = Button(
        win,
        text="Экспорт в CSV",
        width=25,
        height=2,
        command=lambda: export_csv(cipher)
    )

    btn_export.pack(expand=True)
