from pydantic import BaseModel
from typing import Optional

class VacancySchemaBase(BaseModel):
    """Базовая схема для создания/обновления вакансии"""
    units: int = 1
    dep_id: Optional[int] = None
    pos_id: Optional[int] = None
    status: str = "open"

class VacancyResponseSchema(BaseModel):
    """Схема для вывода вакансии"""
    id: int
    units: int
    dep_id: Optional[int] = None
    pos_id: Optional[int] = None
    status: str

