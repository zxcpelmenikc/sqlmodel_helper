from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
if TYPE_CHECKING:
    from .roles import Roles


class Users(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(max_length=255, unique=True)
    password: str = Field(max_length=255)
    role_id: int = Field(foreign_key="roles.id", default=2)
    role: "Roles" = Relationship(back_populates="user_role")

