from pydantic import BaseModel


class Password(BaseModel):
    login: str
    password: str
    description: str

class PasswordForChange(Password):
    id: int
