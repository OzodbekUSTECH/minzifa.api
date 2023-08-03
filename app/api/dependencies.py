from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database.config import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.users import UsersService
from repositories.users import UsersRepository
from typing import Annotated
from services.categories import CategoriesService
from jose import JWTError, jwt
from services.users import SECRET_KEY, ALGORITHM
from schemas.users import TokenData
from repositories.categories import CategoriesRepository
from models import User

def users_service(session: AsyncSession = Depends(get_async_session)):
    return UsersService(UsersRepository(session))

def categories_service(session: AsyncSession = Depends(get_async_session)):
    return CategoriesService(CategoriesRepository(session))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(users_service: Annotated[UsersService, Depends(users_service)], token: str = Depends(oauth2_scheme), ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,   
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # "sub" is the key used by JWT to represent the subject (usually user ID or email)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await users_service.get_user_by_email(token_data.email)
    
    if user is None:
        raise credentials_exception

    return user


class PermissionChecker:

    def __init__(self, required_permission_id: int):
        self.required_permission_id = required_permission_id

    async def __call__(self,  cats_service:  Annotated[CategoriesService, Depends(categories_service)], user: User = Depends(get_current_user)) -> bool:
        category = await cats_service.get_cat_by_id(user.category_id)
        if category:
            for permission in category.permissions:
                if permission["id"] == self.required_permission_id and permission["has_access"]:
                    return True

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Insufficient permissions'
        )