from repositories.base import AbstractRepository, Pagination
from schemas.categories import PermissionUpdate, PermessionSchema, CategorySchema, CatSchemaAdd
from fastapi import HTTPException


class CategoriesService:
    def __init__(self, categories_repo: AbstractRepository):
        self.categories_repo: AbstractRepository = categories_repo

    async def create_category(self, category: CatSchemaAdd):
        
        category_dict = category.model_dump()

        new_category = await self.categories_repo.add_one(category_dict) 
        return new_category
    
    async def get_cat_by_id(self, category_id: int):
        category = await self.categories_repo.find_one(category_id)
        return category
    

    async def update_permission_in_category(self, category_id: int, permission_id: int, permisson_data: PermissionUpdate):
        # Get the category by its ID
        category = await self.categories_repo.find_one(permission_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        permission_to_update = None
        for permission in category.permissions:
            if permission["id"] == permission_id:
                permission_to_update = permission
                break

        if not permission_to_update:
            raise HTTPException(status_code=404, detail="Permission not found in the category")

        permission_to_update["has_access"] = permisson_data.has_access

        data = CategorySchema(
            id=category.id,
            name=category.name,
            permissions=category.permissions
        )

        data_dict = data.model_dump()

        # Update the category in the repository
        updated_category = await self.categories_repo.update_one(category_id, data_dict)

        return updated_category


    async def update_category(self, cat_id: int, category_data: dict):
        # Assuming you have a repository instance for categories (users_repo) in the service
        return await self.categories_repo.update_one(cat_id, category_data)
