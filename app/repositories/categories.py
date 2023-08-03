from models.categories import Category
from repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession

class CategoriesRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Category