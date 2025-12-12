from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.employees_controller import (
    add_employee, 
    get_employees, 
    get_employees_by_department as ged, 
    change_employee_info as cei, 
    change_employee_position as cep, 
    get_unoctive_employees as gue
)
from app.controllers.departments_controller import change_department_info, get_department
from app.controllers.staffing_table_controller import change_staffing_table_info as csti, get_staffing_with_dept_rel as gswdr
from fastapi_pagination import Page
from app.schemas.employees import EmployeeSchema
from app.models.employees import Employees

from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required

from app.schemas.employees_chema import EmployeeSchemaBase as ESUI, EmployeeResponseSchema



router = APIRouter()

@router.post("/add_employee", tags=["Работники"], 
             description="Добавить работника/принять его на работу. "
                        "**Доступ:** Администратор, HR-менеджер. "
                        "**Возможности:** Создание новой записи о сотруднике в системе с полной информацией "
                        "(ФИО, табельный номер, отдел, должность, ИНН, СНИЛС, личные данные, дата приема). "
                        "**Требуемые данные:** Все обязательные поля сотрудника согласно схеме EmployeeSchemaBase.",
             response_model=Employees,summary="Добавить(заполнить карточку) работника")
def add_employee_route(form_data: ESUI, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return add_employee(form_data, session)

@router.get("/employees", tags=["Работники"], 
            description="Получить список всех работников с пагинацией. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Просмотр полного списка сотрудников организации с информацией о каждом. "
                      "Результаты возвращаются с пагинацией для удобной навигации. "
                      "**Параметры:** page (номер страницы), size (размер страницы).",
            response_model=Page[EmployeeResponseSchema],summary="Вывести список всех работников")
def list_employees_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return get_employees(session)



@router.get("/employees_by_department/{department_id}", tags=["Работники"], 
            description="Получить список работников конкретного отдела. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Просмотр всех сотрудников указанного отдела с их должностями. "
                      "**Параметры:** department_id (ID отдела). "
                      "**Возвращает:** Список сотрудников с информацией: ID, имя, фамилия, название должности.",
            response_model=list[EmployeeSchema],summary="Вывести список работников конкретного отдела")
def employees_by_department(department_id: int, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return ged(department_id, session)

@router.put("/employee/{id}", tags=["Работники"], 
            description="Изменить информацию о работнике. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Обновление любых данных сотрудника (личные данные, отдел, должность, "
                      "статус активности и т.д.). Можно обновить как все поля, так и только измененные. "
                      "**Параметры:** id (ID сотрудника), данные для обновления согласно схеме EmployeeSchemaBase.",
            response_model=EmployeeResponseSchema,summary="Изменить карточку работника")
def update_employee_info(id: int, form_data: ESUI, session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return cei(id, form_data, session)

@router.put("/employees_changed_position/{position_id}", tags=["Работники"], 
            description="Перевести работника на новую должность. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Изменение должности сотрудника без изменения других данных. "
                      "Используется для кадровых перемещений и переводов. "
                      "**Параметры:** id (ID сотрудника в URL), position_id (ID новой должности в URL).",
            response_model=Employees,summary="Перевести работника на новую должность")
def employees_changed_position(id: int, position_id:int,  session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return cep(id,position_id, session)

@router.get("/fired_employees", tags=["Работники"], 
            description="Получить список уволенных работников. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Просмотр всех сотрудников со статусом is_active=False (уволенные). "
                      "Результаты возвращаются с пагинацией. "
                      "**Параметры:** page (номер страницы), size (размер страницы).",
            response_model=Page[Employees],summary="Вывести список уволенных работников")
def list_fired_employees_route(session: Session = Depends(get_session), current_user: Users = Depends(admin_or_hr_required)):
    return gue(session)