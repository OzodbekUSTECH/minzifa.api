from repositories.base import AbstractRepository, Pagination
from passlib.context import CryptContext
from schemas.users import UserSchemaAdd
from fastapi import HTTPException, status
from datetime import timedelta, datetime
from jose import  jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



    
class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo

    async def register_user(self, user: UserSchemaAdd):
        existing_user = await self.users_repo.find_one_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user_dict = user.model_dump()
        hashed_password = pwd_context.hash(user.password)
        user_dict['password'] = hashed_password
        new_user = await self.users_repo.add_one(user_dict) 
        return new_user

    async def get_users(self, pagination: Pagination):
        users = await self.users_repo.find_all(pagination)
        return users
    
    async def get_user_by_id(self, user_id: int):
        user = await self.users_repo.find_one(user_id)
        return user
    
    async def get_user_by_email(self, user_email: str):
        user = await self.users_repo.find_one_by_email(user_email)

        return user
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.users_repo.find_one_by_email(email)
        if not user and not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "Bearer"}
        
    # async def update_user(self,user_id: int, user: UserSchemaUpdate):
    #     user_dict = user.model_dump()
        
    #     updated_user = await self.users_repo.update_one(user_id, user_dict)
    #     return updated_user
    


