from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(gt=0, lt=120, index=True)
    email: EmailStr = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(min_length=8, max_length=12)
