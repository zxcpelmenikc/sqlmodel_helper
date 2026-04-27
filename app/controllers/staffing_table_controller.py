from app.db.database import engine
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.staffing_table import Staffing_table
from app.models.departments import Departments
from app.models.employees import Employees
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
    
        session.add(result)
        session.commit()
        session.refresh(result)
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
        # Keep ids (dep_id/pos_id) for editing, add readable names.
        rec = s.dict()
        rec["department_name"] = s.department.name_dep if s.department else None
        rec["position_name"] = s.position.name_position if s.position else None
        result.append(rec)
  
    return result

def update_units_in_staffing_table(session: Session) -> List[Staffing_table]:
    """
    Подсчитывает количество работников с теми же dep_id и pos_id для каждой записи
    в staffing_table и обновляет поле units.
    
    Args:
        session: Сессия базы данных
        
    Returns:
        Список обновленных записей Staffing_table
    """
    try:
        # Получаем все записи staffing_table
        stmt = select(Staffing_table)
        all_staffing = session.exec(stmt).all()
        
        updated_records = []
        
        for staffing_record in all_staffing:
            dep_id = staffing_record.dep_id
            pos_id = staffing_record.pos_id
            
            # Если dep_id или pos_id не указаны, устанавливаем units = 0
            if dep_id is None or pos_id is None:
                staffing_record.units = 0
                session.add(staffing_record)
                updated_records.append(staffing_record)
                continue
            
            # Подсчитываем количество работников с теми же department_id и position_id
            stmt_employees = select(Employees).where(
                Employees.department_id == dep_id,
                Employees.position_id == pos_id
            )
            employees = session.exec(stmt_employees).all()
            count = len(employees)
            
            # Обновляем поле units
            staffing_record.units = count
            session.add(staffing_record)
            updated_records.append(staffing_record)
        
        session.commit()
        
        # Обновляем объекты в сессии
        for record in updated_records:
            session.refresh(record)
        
        return updated_records
        
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера при обновлении units: {str(e)}"
        )

