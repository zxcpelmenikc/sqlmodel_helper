from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import add_employee, get_employees, get_employees_by_department as ged, change_employee_info as cei, change_employee_position as cep, get_unoctive_employees as gue
from app.controllers.departments_controller import change_department_info, get_department
from app.controllers.staffing_table_controller import change_staffing_table_info as csti, get_staffing_with_dept_rel as gswdr
from fastapi_pagination import Page
from app.schemas.employees import EmployeeSchema
from app.models.employees import Employees

from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required

from app.schemas.employees_chema import EmployeeSchemaBase as ESUI, EmployeeResponseSchema



router = APIRouter()

@router.post("/add_employee", tags=["Работники"], description="Добавить работника/принять его на работу", response_model=Employees)
def add_employee_route(form_data: ESUI, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return add_employee(form_data, session)

@router.get("/employees", response_model=Page[EmployeeResponseSchema], tags=["Работники"], description="Вывести список всех работников")
def list_employees_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return get_employees(session)



# GET для списка штатных позиций с именем департамента
@router.get("/employees_by_department/{department_id}", response_model=list[EmployeeSchema], tags=["Работники"], description="Вывести список работников по отделениям") 
def employees_by_department(department_id: int, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return ged(department_id, session)

@router.put("/employee/{id}", tags=["Работники"], description="Изменить информация о работнике ", response_model=EmployeeResponseSchema)
def update_employee_info(id: int, form_data: ESUI, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return cei(id, form_data, session)

@router.put("/employees_changed_position/{position_id}", tags=["Работники"], description="Перевод работника на новую должность")
def employees_changed_position(id: int, position_id:int,  session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return cep(id,position_id, session)

@router.get("/fired_employees", response_model= Page[Employees],tags=["Работники"], description="Вывести список уволеных работников")
def list_fired_employees_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return gue(session)