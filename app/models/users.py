from sqlalchemy.orm import Mapped, mapped_column
from database.config import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)

    
   

