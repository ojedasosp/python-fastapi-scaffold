from fastapi import APIRouter, status

from auth.auth_service import AuthServiceDep
from dtos.auth_dto import Token, UserCredentials

auth_router = APIRouter()

@auth_router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_acces_token(body: UserCredentials, service: AuthServiceDep) -> Token:
    return await service.authenticate_user(body.email, body.password)
