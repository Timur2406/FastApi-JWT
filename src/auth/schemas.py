from pydantic import BaseModel


class Subject(BaseModel):
    username: str
    scopes: int
    banned: bool