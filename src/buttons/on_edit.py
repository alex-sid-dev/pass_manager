from tkinter import ttk, messagebox

from src.buttons.open_edit_window import open_edit_window
from src.crypto_utils.crypto import PasswordCipher


def edit_selected(tree: ttk.Treeview, cipher: PasswordCipher):
    selected = tree.selection()
    if len(selected) != 1:
        messagebox.showwarning("Внимание", "Выберите одну запись для редактирования")
        return

    item = selected[0]
    id, login, password, description = tree.item(item, "values")
    open_edit_window(tree, id, item, login, password, description, cipher)

