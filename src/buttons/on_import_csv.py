import csv
from tkinter import messagebox, filedialog

from src.crypto_utils.crypto import PasswordCipher
from src.database.create_password import create_password
from src.models.passwords import Password


def import_csv(cipher: PasswordCipher):
    file_path = filedialog.askopenfilename(
        title="Выберите CSV файл",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    imported = 0
    errors = 0

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            required_fields = {"name", "username", "password"}
            if not required_fields.issubset(reader.fieldnames):
                messagebox.showerror(
                    "Ошибка",
                    "CSV файл имеет неверную структуру"
                )
                return

            for row in reader:
                try:
                    login = row["username"].strip()
                    raw_password = row["password"]
                    description = row["name"].strip()

                    if not login or not raw_password:
                        continue

                    # 🔐 если нужно шифрование
                    encrypted_password = cipher.encrypt(raw_password)

                    pwd = Password(
                        login=login,
                        password=encrypted_password,
                        description=description
                    )

                    create_password(pwd)
                    imported += 1

                except Exception:
                    errors += 1

        messagebox.showinfo(
            "Импорт завершён",
            f"Импортировано: {imported}\nОшибок: {errors}"
        )

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
