from pydantic import BaseModel
from typing import Optional

class PositionSchemaBase(BaseModel):
    """Базовая схема для создания/обновления позиции"""
    name_position: str
    code_position: str

class PositionResponseSchema(BaseModel):
    """Схема для вывода позиции"""
    id_pos: int
    name_position: str
    code_position: str

