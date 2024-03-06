from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator, SecretStr
import re, string


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    password: SecretStr = Field(min_length=8)
    email: Optional[EmailStr] = None

    @validator('password')
    def check_password(cls, value: SecretStr):
        special_characters = re.escape(string.punctuation)
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[' + special_characters + r'])', value.get_secret_value()):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву, одну цифру, один спецсимвол и одну маленькую букву.')
        return value
    

class UserAuth(BaseModel):
    username: str
    password: SecretStr

