from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import add_employee, get_employees, get_employees_by_department as ged, change_employee_info as cei, change_employee_position as cep
from app.controllers.departments_controller import change_department_info, get_department
from app.controllers.staffing_table_controller import (
    change_staffing_table_info as csti, 
    get_staffing_with_dept_rel as gswdr,
    update_units_in_staffing_table
)
from fastapi_pagination import Page
from app.schemas.employees import EmployeeSchema
from app.models.employees import Employees
from app.models.staffing_table import Staffing_table
from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required
from app.models.departments import Departments



router = APIRouter()


@router.get("/staffing_table", tags=["Штатное расписание"], 
            description="Получить штатное расписание с расширенной информацией. "
                      "**Доступ:** Все пользователи (без авторизации). "
                      "**Возможности:** Просмотр штатного расписания с названиями отделов и должностей "
                      "вместо только ID. Включает информацию о количестве единиц, зарплатах, надбавках. "
                      "**Возвращает:** Список записей штатного расписания с полными названиями отделов и должностей.",
            response_model=list)
def get_staffing_with_dept_rel_route(session: Session = Depends(get_session)):
    return gswdr(session)

@router.put("/staffing_table/{id}", tags=["Штатное расписание"], 
            description="Изменить запись в штатном расписании. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Обновление данных штатного расписания (количество единиц, зарплата, "
                      "надбавки, общая зарплата, детали). Можно обновить как все поля, так и только измененные. "
                      "**Параметры:** id (ID записи штатного расписания), данные для обновления согласно модели Staffing_table.",
            response_model=Staffing_table)
def update_staffing_info(id: int, data: Staffing_table, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return csti(id, data, session)

@router.post("/staffing_table/update_units", tags=["Штатное расписание"], 
             description="Автоматически обновить количество работников (единицы) для всех записей штатного расписания. "
                        "**Доступ:** Администратор, HR-менеджер. "
                        "**Возможности:** Автоматический пересчет поля units (количество единиц) для каждой записи "
                        "штатного расписания на основе реального количества сотрудников с соответствующими "
                        "department_id и position_id. Полезно после массовых изменений в данных сотрудников. "
                        "**Возвращает:** Список обновленных записей штатного расписания.",
             response_model=list[Staffing_table])
def update_units_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return update_units_in_staffing_table(session)