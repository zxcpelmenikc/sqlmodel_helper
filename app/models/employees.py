from typing import Optional,List
from decimal import Decimal
from sqlmodel import SQLModel, Field,Relationship
from datetime import date
class Employees(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    last_name: str = Field(max_length= 100)
    first_name: str = Field(max_length= 100)
    middle_name: str = Field(max_length= 100)
    tab_number: int = Field(max_length=20)
    inn: str = Field(max_length=12)
    snils: str = Field(max_length=14)
    gender: str = Field(max_length=20)
    birth_date: date = Field
    birth_place: str = Field(max_length=255)
    address: str = Field(max_length=500)
    education: str = Field(max_length=100)
    profession: str = Field(max_length=100)
    marital_status: str = Field(max_length=50)
    hire_date: date = Field
    dismissal_date: date = Field
    is_active: bool = Field(default=True, index=True)