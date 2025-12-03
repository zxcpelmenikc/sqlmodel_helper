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

# class EmployeeSchemaUpdateInfo(EmployeeSchemaBase):
#     @classmethod
#     def as_form(cls,
#         last_name: str = Form(..., description="Имя пользователя"),
#         first_name: str = Form(..., description="Пароль"),
#         middle_name: str = Form(..., description="отчество"),
#         tab_number: int = Form(..., description="Табельный номер"),
#         department_id: int = Form(..., description="ID отдела"),
#         position_id: int = Form(..., description="ID должности"),   
#         inn: str = Form(..., description="ИНН"),
#         snils: str = Form(..., description="СНИЛС"),
#         gender: str = Form(..., description="Пол"),
#         birth_date: date = Form(..., description="Дата рождения"),
#         birth_place: str = Form(..., description="Место рождения"),
#         address: str = Form(..., description="Адрес"),
#         education: str = Form(..., description="Образование"),
#         profession: str = Form(..., description="Профессия"),
#         marital_status: str = Form(..., description="Семейное положение"),
#         hire_date: date = Form(..., description="Дата приема на работу"),
#         dismissal_date: date = Form(None, description="Дата увольнения"),
#         is_active: bool = Form(..., description="Активен ли сотрудник")
#     ):
#         return cls(
#             last_name=last_name, first_name=first_name, middle_name=middle_name,
#             tab_number=tab_number, department_id=department_id, position_id=position_id,
#             inn=inn, snils=snils, gender=gender, birth_date=birth_date, birth_place=birth_place,
#             address=address, education=education, profession=profession, marital_status=marital_status,
#             hire_date=hire_date, dismissal_date=dismissal_date, is_active=is_active
#         )

