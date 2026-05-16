from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from pydantic import EmailStr
from dtos.user_dto import UserPublic
from users.user_service import UserServiceDep
from . import get_password_hash, verify_password
from config import config

class AuthRepository:

    def __init__(self, user_service: UserServiceDep) -> None:
        self._user_service = user_service

    async def authenticate(self, email: EmailStr, password: str) -> UserPublic | None:
        user = await self._user_service.get_user_by_email(email)
        if not verify_password(user.password, get_password_hash(password)):
            return None
        return UserPublic(**user.model_dump(exclude_unset=True))
 
    def create_access_token(self, data: dict, expire_delta: timedelta | None = None):
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
        return encoded_jwt

    async def current_user(self, token: str):
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        email = payload.get("sub")
        if email is None:
            return None
        user = await self._user_service.get_user_by_email(email)
        if user is None:
            return None
        return user

def get_auth_repository(user_service: UserServiceDep) -> AuthRepository:
    return AuthRepository(user_service)

AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
