from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.departments import Departments
    from app.models.positions import Positions

class Staffing_table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Ссылки на PK целевых таблиц (обязательно уникальные/PK)
    dep_id: Optional[int] = Field(default=None, foreign_key="departments.id_dep")
    pos_id: Optional[int] = Field(default=None, foreign_key="positions.id_pos")

    units: int = Field(default=1)
    units_needed: int = Field(default=1)
    salary: Optional[float] = Field(default=0)
    nadbavki: Optional[float] = Field(default=0)
    total_salary: Optional[float] = Field(default=0)
    details: Optional[str] = Field(default=None, max_length=255)

    # Отношения (forward refs) — проверьте, что в Departments/Positions есть back_populates="staffing_tables"
    department: Optional["Departments"] = Relationship(back_populates="staffing_tables")
    position: Optional["Positions"] = Relationship(back_populates="staffing_tables")