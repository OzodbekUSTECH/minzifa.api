from pydantic import BaseModel, validator, EmailStr

class CatSchemaAdd(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    has_access: bool


class PermessionSchema(BaseModel):
    id: int
    name: str
    endpoint_req: str
    has_access: bool

    


class CategorySchema(BaseModel):
    id: int
    name: str
    permissions: list[PermessionSchema]