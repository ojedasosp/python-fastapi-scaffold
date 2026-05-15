from fastapi import APIRouter, status, Query
from dtos import CreateUserDTO, UpdateUserDTO, UserPublic
from users.user_service import UserServiceDep

user_router = APIRouter()

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def get_users(service: UserServiceDep, offset: int = 0, limit: int = Query(default=10, le=100)):
    return await service.get_users(offset, limit)

@user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def get_user(id: int, service: UserServiceDep):
    return await service.get_user(id)

@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(user: CreateUserDTO, service: UserServiceDep):
    return await service.create_user(user)


@user_router.put("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def update_user(id: int, user: UpdateUserDTO, service: UserServiceDep):
    return await service.update_user(id, user)

@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, service: UserServiceDep):
    await service.delete_user(id)
