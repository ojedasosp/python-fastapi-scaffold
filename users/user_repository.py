from typing import Annotated, Sequence
from fastapi import Depends
from pydantic import EmailStr
from database import SessionDep
from users.user_entity import User
from dtos import CreateUserDTO, UpdateUserDTO
from sqlmodel import select

class UserRepository:

    def __init__(self, session: SessionDep) -> None:
        self._session = session

    async def create(self, user: CreateUserDTO) -> User:
        async with self._session as session:
           new_user = User(**user.model_dump(exclude_unset=True))
           session.add(new_user)
           await session.commit()
           await session.refresh(new_user)
           return new_user

    async def find_by_id(self, id: int) -> User | None:
        async with self._session as session:
            user = await session.get(User, id)
            return user

    async def update(self,id: int, user: UpdateUserDTO) -> User | None:
        async with self._session as session:
            db_user = await self.find_by_id(id)
            user_data = user.model_dump(exclude_unset=True) 
            if not db_user:
                return None
            db_user.sqlmodel_update(user_data)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    async def find_by_email(self, email: EmailStr) -> User | None: 
        async with self._session as session:
            statement = select(User).where(User.email ==  email)
            result = await session.execute(statement)
            return result.scalars().one_or_none()
 
    async def delete(self, user: User) -> None:
        async with self._session as session:
            await session.delete(user)
            await session.commit()

    async def users(self, offset: int, limit: int) -> list[User]:
        async with self._session as session:
           users = await session.execute(select(User).offset(offset).limit(limit))
           return list(users.scalars().all())




def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session=session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
