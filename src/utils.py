import string
import random

def generate_password(length=12):
    chars = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*()-_=+[]{};:,.<>?"
    )
    return ''.join(random.choice(chars) for _ in range(length))
