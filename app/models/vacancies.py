from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.positions import Positions
    from app.models.departments import Departments

class Vacancies(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    units: int = Field(default=1)
    dep_id: Optional[int] = Field(default=None, foreign_key="departments.id_dep")
    pos_id: Optional[int] = Field(default=None, foreign_key="positions.id_pos")
    status: str = Field(default="open", max_length=50)

    position: Optional["Positions"] = Relationship(back_populates="vacancies")
    department: Optional["Departments"] = Relationship(back_populates="vacancies")