from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import add_employee, get_employees, get_employees_by_department as ged, change_employee_info as cei, change_employee_position as cep
from app.controllers.departments_controller import change_department_info, get_department
from app.models.users import Users
from app.core.security import admin_required
from app.models.departments import Departments

router = APIRouter()

@router.get("/departments",tags=["departments"], description="Вывести все отделения")
def list_department_route(session: Session = Depends(get_session)):
    return get_department(session)

@router.put("/department/{id_dep}",tags=["departments"], description="Изменить данные отделения")
def update_department_route(id_dep: int, data: Departments, session: Session = Depends(get_session),current_user: Users = Depends(admin_required)):
    return change_department_info(id_dep, data, session)