from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import add_employee, get_employees, get_employees_by_department as ged, change_employee_info as cei, change_employee_position as cep
from app.controllers.departments_controller import change_department_info, get_department
from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required
from app.models.departments import Departments

router = APIRouter()

@router.get("/departments", tags=["Отделы"], 
            description="Получить список всех отделов организации. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Просмотр всех отделов с их названиями и кодами. "
                      "**Возвращает:** Список всех отделов с полной информацией.",
            response_model=list[Departments],summary="Вывести список всех отделов")
def list_department_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return get_department(session)

@router.put("/department/{id_dep}", tags=["Отделы"], 
            description="Изменить данные отдела. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Обновление информации об отделе (название, код отдела). "
                      "**Параметры:** id_dep (ID отдела), данные для обновления согласно модели Departments.",
            response_model=Departments,summary="Изменить данные отдела")
def update_department_route(id_dep: int, data: Departments, session: Session = Depends(get_session),current_user: Users = Depends(admin_or_hr_required)):
    return change_department_info(id_dep, data, session)