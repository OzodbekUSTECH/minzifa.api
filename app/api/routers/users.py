from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import users_service, PermissionChecker
from api.utils import Pagination
from schemas.users import UserSchemaAdd, UserSchema, Token
from services.users import UsersService
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("", response_model=UserSchema)
async def add_user(
    user_data: UserSchemaAdd,
    users_service: Annotated[UsersService, Depends(users_service)],
):
    user = await users_service.register_user(user_data)
    return user

@router.get("", response_model=list[UserSchema], dependencies=[Depends(PermissionChecker(required_permission_id=1))])
async def get_users(
    users_service: UsersService = Depends(users_service),
    pagination: Pagination = Depends()
):
    users = await users_service.get_users(pagination)
    return users

@router.get("/{id}")
async def get_user_perms(
    id: int, 
    users_service: UsersService = Depends(users_service),
):
    user = await users_service.get_user_by_id(id)
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users_service: Annotated[UsersService, Depends(users_service)]
):
    access_token = await users_service.authenticate_user(form_data.username, form_data.password)
    return access_token