from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from app.models.employment_history import EmploymentHistory
    from app.models.departments import Departments
    from app.models.positions import Positions

class Employees(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str = Field(max_length=100)
    first_name: str = Field(max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    tab_number: Optional[int] = Field(default=None)
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id_dep")
    position_id: Optional[int] = Field(default=None, foreign_key="positions.id_pos")
    inn: Optional[str] = Field(default=None, max_length=12)
    snils: Optional[str] = Field(default=None, max_length=14)
    gender: Optional[str] = Field(default=None, max_length=20)
    birth_date: Optional[date] = Field(default=None)
    birth_place: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=500)
    education: Optional[str] = Field(default=None, max_length=100)
    profession: Optional[str] = Field(default=None, max_length=100)
    marital_status: Optional[str] = Field(default=None, max_length=50)
    hire_date: Optional[date] = Field(default=None)
    dismissal_date: Optional[date] = Field(default=None)
    is_active: bool = Field(default=True, index=True)



    position: Optional["Positions"] = Relationship(back_populates="employees")
    department: Optional["Departments"] = Relationship(back_populates="employees")
    employment_history: List["EmploymentHistory"] = Relationship(back_populates="employee")