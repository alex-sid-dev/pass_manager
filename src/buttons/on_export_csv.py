import csv
from tkinter import filedialog, messagebox

from src.crypto_utils.crypto import PasswordCipher
from src.database.read_password import get_all_passwords


def export_csv(cipher: PasswordCipher):
    file_path = filedialog.asksaveasfilename(
        title="Сохранить CSV",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    try:
        rows = get_all_passwords()

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["name", "url", "username", "password", "note"]
            )

            writer.writeheader()

            for login, encrypted_password, description in rows:
                # 🔓 если нужно расшифровать
                password = cipher.decrypt(encrypted_password)

                writer.writerow({
                    "name": description or "",
                    "url": "",
                    "username": login,
                    "password": password,
                    "note": ""
                })

        messagebox.showinfo(
            "Экспорт завершён",
            f"Экспортировано записей: {len(rows)}"
        )

    except Exception as e:
        messagebox.showerror("Ошибка экспорта", str(e))
