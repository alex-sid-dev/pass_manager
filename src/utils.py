import random
import string


class PasswordGenerator:
    length = 12

    @classmethod
    def generate_password(cls):
        chars = (
                string.ascii_lowercase +
                string.ascii_uppercase +
                string.digits +
                "!@#$%^&*()-_=+[]{};:,.<>?"
        )
        return ''.join(random.choice(chars) for _ in range(cls.length))
