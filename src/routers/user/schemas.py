from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserUpdate(BaseModel):
    username: Optional[str] = None
    scopes: Optional[int] = None
    banned: Optional[bool] = None


class UserResponse(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    registration_date: int


class UserQuery(BaseModel):
    username: Optional[str] = Field(min_length=1, max_length=32)


class UserDTO(BaseModel):
    username: str
    hashed_password: str
    email: Optional[EmailStr] = None
    registration_date: int
    scopes: int
    banned: bool

