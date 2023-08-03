from abc import ABC, abstractmethod
from fastapi import Query
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from api.utils import Pagination





class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError
    
    @abstractmethod
    async def find_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_one_by_email():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
        raise NotImplementedError


from sqlalchemy.orm import selectinload

class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = None  # Set the model based on the resource (users, posts, etc.)

    # Rest of the code remains the same...

    async def add_one(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().one()
    
    async def find_all(self, pagination: Pagination) -> list:
        stmt = select(self.model)
        stmt = stmt.order_by("id").offset(pagination.offset).limit(pagination.limit)  # Add pagination parameters
        res = await self.session.execute(stmt)
        # res = [row[0].to_read_model() for row in res.all()]
        return res.scalars()

        
    async def find_one(self, id: int) -> dict:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        # response = res.fetchone()[0].to_read_model()
        return res.scalars().one()
        
    async def find_one_by_email(self, email: str) -> dict:
        stmt = select(self.model).where(self.model.email == email)
        res = await self.session.execute(stmt)
        try:
            return res.scalars().one()
        except NoResultFound:
            return None 
    
    async def update_one(self, id: int, data: dict) -> dict:
        stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalars().one()


    async def delete_one(self, id: int) -> dict:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.fetchone()[0].to_read_model()
