from sqlalchemy.orm import Mapped, mapped_column
from database.config import Base
from sqlalchemy import JSON
from models.permissions.permissions_json import perms_json

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]

    permissions: Mapped[str] = mapped_column(JSON, default=perms_json)
    
    