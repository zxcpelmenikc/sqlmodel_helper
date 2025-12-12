from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.staffing_table import Staffing_table
    from app.models.vacancies import Vacancies
    from app.models.employees import Employees

class Positions(SQLModel, table=True):
    id_pos: int= Field(default=None, primary_key=True)
    name_position: str = Field(max_length=100)
    code_position: str = Field(max_length=20)



    employees: List["Employees"] = Relationship(back_populates="position")
    staffing_tables: List["Staffing_table"] = Relationship(back_populates="position")
    vacancies: List["Vacancies"] = Relationship(back_populates="position")