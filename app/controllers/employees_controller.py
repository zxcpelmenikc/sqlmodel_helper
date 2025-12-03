from app.models.employees import Employees
from app.models.positions import Positions
from sqlmodel import Session, select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
import json
from fastapi_pagination import paginate, Params

def add_employee(data, session: Session):
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

        employee = Employees(**payload)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {e}")

def get_employees(session: Session,  page: int = 1, size: int = 19) -> List[Employees]:
    try:
        sql = select(Employees)
        result = session.exec(sql).all()
        return paginate(result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
    

def get_employees_by_department(id_dep:int, session: Session):
    try:
        stmt = (
            select(
                Employees.id,
                Employees.first_name,
                Employees.last_name,
                Positions.name_position
            )
            .join(Positions, Employees.position_id == Positions.id_pos, isouter=True)
            .where(Employees.department_id == id_dep)
        )
        rows = session.exec(stmt).all()
        items = []
        for id, first_name, last_name, position_name in rows:
            items.append({
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "position_name": position_name
            })
        
        return items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
    

def change_employee_info(id: int, data, session: Session) -> Employees:
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

        result = session.get(Employees, id)
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
    

def change_employee_position(id: int, position_id: int, session: Session, ) -> Employees:
    try:
        employee = session.get(Employees, id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="идентификатор не найден")

        employee.position_id = position_id
        session.commit()
        session.refresh(employee)
        return employee
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
    
def get_unoctive_employees(session: Session,  page: int = 1, size: int = 19) -> List[Employees]:
    try:
        sql = select(Employees).where(Employees.is_active== False)
        result = session.exec(sql).all()
        return paginate(result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")