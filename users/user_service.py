from typing import Annotated
from fastapi import Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError, OperationalError

from dtos import CreateUserDTO, UpdateUserDTO
from users.user_entity import User
from users.user_repository import UserRepositoryDep

class UserService:

    def __init__(self, repository: UserRepositoryDep) -> None:
       self._repository = repository 


    async def get_user(self, id: int) -> User:
        try:
            user = await self._repository.find_by_id(id)
            if not user:
                raise HTTPException(status_code=404,detail="user not found")
            return user
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavaiable")

    async def update_user(self, id: int, user: UpdateUserDTO) -> User:
        try:
            updated_user = await self._repository.update(id,user)
            if not updated_user:
                raise HTTPException(status_code=404, detail="user not found")
            return updated_user
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavaiable")

    async def create_user(self, user: CreateUserDTO):
        try:
            created_user = await self._repository.create(user)
            if not created_user:
                raise HTTPException(status_code=400, detail="cannot create user")
            return created_user
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavaiable")
        except IntegrityError:
            raise HTTPException(status_code=409,detail="user already exists")

    async def delete_user(self, id: int):
        try:
            user = await self.get_user(id)
            await self._repository.delete(user)
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavaiable")

    async def get_users(self, offset: int, limit: int) -> list[User]:
        try:
            users = await self._repository.users(offset, limit)
            return users
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavailable")

    async def get_user_by_email(self, email: EmailStr) -> User:
        try:
            user = await self._repository.find_by_email(email)
            if user is None:
                raise HTTPException(status_code=404, detail="not found")
            return user
        except OperationalError:
            raise HTTPException(status_code=509, detail="database unavailable")






def get_user_service(repository: UserRepositoryDep):
    return UserService(repository)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
