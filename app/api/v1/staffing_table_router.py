from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import add_employee, get_employees, get_employees_by_department as ged, change_employee_info as cei, change_employee_position as cep
from app.controllers.departments_controller import change_department_info, get_department
from app.controllers.staffing_table_controller import change_staffing_table_info as csti, get_staffing_with_dept_rel as gswdr
from fastapi_pagination import Page
from app.schemas.employees import EmployeeSchema
from app.models.employees import Employees
from app.models.staffing_table import Staffing_table
from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required
from app.models.departments import Departments



router = APIRouter()


@router.get("/staffing_table", tags=["Штатное расписание"], description= "Вывод расписания с названием должности и департамента")
def get_staffing_with_dept_rel_route(session: Session = Depends(get_session)):
    return gswdr(session)

@router.put("/staffing_table/{id}",tags=["Штатное расписание"], description= "Изменение расписания")
def update_staffing_info(id: int, data: Staffing_table, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return csti(id, data, session)