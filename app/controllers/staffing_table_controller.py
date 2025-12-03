from app.db.database import engine
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.staffing_table import Staffing_table
from app.models.departments import Departments
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from typing import List
import json

def change_staffing_table_info(id: int, data, session: Session) -> Staffing_table:
    try:
        # Нормализуем payload в dict
        if hasattr(data, "dict"):
            payload = data.dict(exclude_unset=True)
        elif isinstance(data, dict):
            payload = data
        elif isinstance(data, str):
            try:
                payload = json.loads(data)
                if not isinstance(payload, dict):
                    
                    raise ValueError
            except json.JSONDecodeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Неверный формат JSON в теле запроса")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Ожидается объект (dict/SQLModel/Pydantic)")

        result = session.get(Staffing_table, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="идентификатор не найден")

        # Обновляем поля
        for key, value in payload.items():
            setattr(result, key, value)
    
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
def get_staffing_with_dept_rel(session: Session):
    stmt = select(Staffing_table).options(selectinload(Staffing_table.department), selectinload(Staffing_table.position))
    staffings = session.exec(stmt).all()  # список Staffing_table
    result = []
    for s in staffings:
        rec = s.dict()
        rec = {k: v for k, v in s.dict().items() if k != "dep_id"}
        rec = {k: v for k, v in s.dict().items() if k != "pos_id"}
        rec["department_name"] = s.department.name_dep if s.department else None
        rec["position_name"] = s.position.name_position if s.position else None
        result.append(rec)
  
    return result

