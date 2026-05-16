from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from pydantic import EmailStr
from auth.auth_repository import AuthRepositoryDep
from config import config
from dtos.auth_dto import Token
from users.user_entity import User
from auth import scheme

class AuthService:

    def __init__(self, auth_repository: AuthRepositoryDep) -> None:
        self._auth_repository = auth_repository

    async def authenticate_user(self, email: EmailStr, password: str) -> Token:
        user = await self._auth_repository.authenticate(email, password)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
        access_token = self._auth_repository.create_access_token({"sub": user.email}, expire_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(scheme)], auth_repository: AuthRepositoryDep) -> User:
       credentials_exception = HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Could not validate credentials",
           headers={"WWW-Authenticate": "Bearer"},
       )
       try:
           user = await auth_repository.current_user(token)
           if user is None:
               raise credentials_exception
           return user
       except InvalidTokenError: 
           raise credentials_exception

CurrentUserDep = Annotated[User, Depends(get_current_user)]

def get_auth_service(auth_repository: AuthRepositoryDep):
   return AuthService(auth_repository)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
