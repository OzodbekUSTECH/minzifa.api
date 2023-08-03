from pydantic import BaseModel, validator, EmailStr


class PermissionSchema(BaseModel):
    id: int
    name: str

class UserSchema(BaseModel):
    id: int
    name: str
    email: str


class UserSchemaAdd(BaseModel):
    name: str
    email: EmailStr
    password: str
    category_id: int

    @validator("name")
    def validate_name_length(cls, v):
        if len(v) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return v
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be at least 5 characters long")
        return v
    


    
class TokenData(BaseModel):
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str