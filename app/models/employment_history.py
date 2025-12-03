from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from app.models.departments import Departments
    from app.models.positions import Positions
    from app.models.employees import Employees

class EmploymentHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employees.id")
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id_dep")
    position_id: Optional[int] = Field(default=None, foreign_key="positions.id_pos")

    start_date: date
    end_date: Optional[date] = Field(default=None)

    salary: Optional[float] = Field(default=None)
    contract_number: Optional[str] = Field(default=None)
    contract_date: Optional[date] = Field(default=None)


    
    employee: Optional["Employees"] = Relationship(back_populates="employment_history")
    department: Optional["Departments"] = Relationship(back_populates="employment_history")
    position: Optional["Positions"] = Relationship(back_populates="employment_history")