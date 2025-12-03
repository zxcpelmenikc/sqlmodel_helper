from app.db.database import engine
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.departments import Departments
from fastapi import Depends
from app.db.session import get_session
from typing import List
import json

def change_department_info(id: int, data, session: Session) -> Departments:
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

        result = session.get(Departments, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="идентификатор не найден")

        # Обновляем поля
        for key, value in payload.items():
            setattr(result, key, value)

        session.commit()
        session.refresh(result)
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def get_department(session: Session) -> List[Departments]:
    try:
        sql = select(Departments)
        result = session.exec(sql).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
