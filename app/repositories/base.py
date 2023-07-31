from abc import ABC, abstractmethod
from fastapi import Query
from sqlalchemy import insert, select, update, delete
from database.config import async_session_maker


class Pagination:
    def __init__(self, page: int = Query(1, ge=1), page_size: int = Query(10, le=100)):
        self.page = page
        self.page_size = page_size
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size




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



class SQLAlchemyRepository(AbstractRepository):
    model = None
    
    
    async def add_one(self, data: dict) -> dict:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.fetchone()[0].to_read_model()
    
    async def find_all(self, pagination: Pagination) -> list:
        async with async_session_maker() as session:
            stmt = select(self.model)
            stmt = stmt.order_by("id").offset(pagination.offset).limit(pagination.limit)  # Add pagination parameters
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

        
    async def find_one(self, id: int) -> dict:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            response = res.fetchone()[0].to_read_model()
            return response
        
    async def find_one_by_email(self, email: str) -> dict:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.email == email)
            res = await session.execute(stmt)
            response = res.fetchone()
            if response is None:
                return None
            return response[0]
    
    async def update_one(self, id: int, data: dict) -> dict:
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.fetchone()[0].to_read_model()


    async def delete_one(self, id: int) -> dict:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.fetchone()[0].to_read_model()
