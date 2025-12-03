from fastapi import Form
from sqlmodel import Field

from pydantic import BaseModel
from fastapi import Form

class EmployeeSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position_name: str


    @classmethod
    def as_form(        cls,
        id: int = Form(..., description="ID сотрудника"),
        first_name: str = Form(..., description="Имя"),
        last_name: str = Form(..., description="Фамилия"),
        position_name: str = Form(..., description="Должность"),
            ):

        return cls(id = id, first_name=first_name, last_name=last_name, position_name=position_name)