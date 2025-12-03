from app.models.positions import Positions
from sqlmodel import Session, select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
import json
from app.schemas.positions_schema import PositionSchemaBase

def create_position(data: PositionSchemaBase, session: Session) -> Positions:
    """Создать новую позицию"""
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
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Неверный формат JSON в теле запроса")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Ожидается объект (dict/SQLModel/Pydantic)")

        # Исключаем id_pos из payload при создании, чтобы БД сгенерировала его автоматически
        payload.pop('id_pos', None)
        
        position = Positions(**payload)
        session.add(position)
        session.commit()
        session.refresh(position)
        return position
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Ошибка: дубликат или нарушение целостности данных: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {e}")

def get_positions(session: Session) -> List[Positions]:
    """Получить все позиции"""
    try:
        sql = select(Positions)
        result = session.exec(sql).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def get_position_by_id(id_pos: int, session: Session) -> Positions:
    """Получить позицию по ID"""
    try:
        position = session.get(Positions, id_pos)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Позиция не найдена")
        return position
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def update_position(id_pos: int, data: PositionSchemaBase, session: Session) -> Positions:
    """Обновить позицию"""
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

        position = session.get(Positions, id_pos)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Позиция не найдена")

        # Обновляем поля
        for key, value in payload.items():
            setattr(position, key, value)

        session.commit()
        session.refresh(position)
        return position
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def delete_position(id_pos: int, session: Session) -> dict:
    """Удалить позицию"""
    try:
        position = session.get(Positions, id_pos)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Позиция не найдена")
        
        session.delete(position)
        session.commit()
        return {"message": "Позиция успешно удалена", "id_pos": id_pos}
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Невозможно удалить позицию: она используется в других таблицах")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

