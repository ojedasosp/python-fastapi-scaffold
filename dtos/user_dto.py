from sqlmodel import SQLModel
from users.user_entity import UserBase
from pydantic import EmailStr



class CreateUserDTO(UserBase):
    password: str

class UpdateUserDTO(SQLModel):
    name: str | None = None
    age: int | None = None
    email: EmailStr | None = None




class UserPublic(UserBase): ...
