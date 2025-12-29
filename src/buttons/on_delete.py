from tkinter import ttk, messagebox

from src.database.delete_password import delete_passwords


def delete_selected(tree: ttk.Treeview):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Ничего не выбрано")
        return

    if not messagebox.askyesno("Подтверждение", f"Удалить {len(selected)} выбранных записей?"):
        return

    for item in selected:
        id, login, password, description = tree.item(item, "values")
        delete_passwords(id=id)  # реализуй удаление по login+description
        tree.delete(item)
