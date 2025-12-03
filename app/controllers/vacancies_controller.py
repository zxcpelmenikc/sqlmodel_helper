from app.models.vacancies import Vacancies
from sqlmodel import Session, select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
import json
from app.schemas.vacancies_schema import VacancySchemaBase

def create_vacancy(data: VacancySchemaBase, session: Session) -> Vacancies:
    """Создать новую вакансию"""
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

        # Исключаем id из payload при создании, чтобы БД сгенерировала его автоматически
        payload.pop('id', None)
        
        vacancy = Vacancies(**payload)
        session.add(vacancy)
        session.commit()
        session.refresh(vacancy)
        return vacancy
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

def get_vacancies(session: Session) -> List[Vacancies]:
    """Получить все вакансии"""
    try:
        sql = select(Vacancies)
        result = session.exec(sql).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def get_vacancy_by_id(id: int, session: Session) -> Vacancies:
    """Получить вакансию по ID"""
    try:
        vacancy = session.get(Vacancies, id)
        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Вакансия не найдена")
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def update_vacancy(id: int, data: VacancySchemaBase, session: Session) -> Vacancies:
    """Обновить вакансию"""
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

        vacancy = session.get(Vacancies, id)
        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Вакансия не найдена")

        # Обновляем поля
        for key, value in payload.items():
            setattr(vacancy, key, value)

        session.commit()
        session.refresh(vacancy)
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

def delete_vacancy(id: int, session: Session) -> dict:
    """Удалить вакансию"""
    try:
        vacancy = session.get(Vacancies, id)
        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Вакансия не найдена")
        
        session.delete(vacancy)
        session.commit()
        return {"message": "Вакансия успешно удалена", "id": id}
    except HTTPException:
        raise
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Невозможно удалить вакансию: она используется в других таблицах")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")

