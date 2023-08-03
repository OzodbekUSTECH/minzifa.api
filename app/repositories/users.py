from models.users import User
from repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User
        