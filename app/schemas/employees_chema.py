from pydantic import BaseModel, field_validator
from fastapi import Form
from sqlmodel import Field
from typing import Optional
from datetime import date

class EmployeeSchemaBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    tab_number: int
    department_id: int
    position_id: int
    inn: str
    snils: str
    gender: str
    birth_date: date
    birth_place: str
    address: str
    education: str
    profession: str
    marital_status: str
    hire_date: date
    dismissal_date: Optional[date] = None
    is_active: bool

    @field_validator('dismissal_date', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

class EmployeeResponseSchema(BaseModel):
    """Схема для вывода сотрудника без поля id"""
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    tab_number: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    address: Optional[str] = None
    education: Optional[str] = None
    profession: Optional[str] = None
    marital_status: Optional[str] = None
    hire_date: Optional[date] = None
    dismissal_date: Optional[date] = None
    is_active: bool


