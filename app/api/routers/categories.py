from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import categories_service

from services.categories import CategoriesService
from api.utils import Pagination
from schemas.categories import CatSchemaAdd, CategorySchema, PermissionUpdate
router = APIRouter(
    prefix="/cats",
    tags=["Cats"],
)


@router.post("")
async def add_cat(
    user_data: CatSchemaAdd,
    users_service: Annotated[CategoriesService, Depends(categories_service)],
):
    user = await users_service.create_category(user_data)
    return user

@router.get("/{id}", response_model=CategorySchema)
async def get_perms(
    id: int,
    users_service: Annotated[CategoriesService, Depends(categories_service)],
):
    cat = await users_service.get_cat_by_id(id)
    return cat

@router.put("/{cat_id}/permissions/{perm_id}", response_model=CategorySchema)
async def update_perm_of_cat(
    cat_id: int,
    perm_id: int,
    perm_data: PermissionUpdate,
    users_service: Annotated[CategoriesService, Depends(categories_service)],
):
    updated_category = await users_service.update_permission_in_category(cat_id, perm_id, perm_data)
    return updated_category

# @router.get("/{id}")
# async def get_user_perms(
#     id: int, 
#     users_service: UsersService = Depends(users_service),
# ):
#     user = await users_service.get_user_by_id(id)
#     return user


