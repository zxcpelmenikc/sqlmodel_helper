from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.staffing_table import Staffing_table
    from app.models.vacancies import Vacancies
    from app.models.employees import Employees

class Departments(SQLModel, table=True):
    id_dep: int = Field(default=None, primary_key=True)
    name_dep: str = Field(max_length=100)
    code_dep: str = Field(max_length=20)



    employees: List["Employees"] = Relationship(back_populates="department")
    staffing_tables: List["Staffing_table"] = Relationship(back_populates="department")
    vacancies: List["Vacancies"] = Relationship(back_populates="department")