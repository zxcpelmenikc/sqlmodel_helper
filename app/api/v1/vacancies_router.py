from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.vacancies_controller import (
    create_vacancy,
    get_vacancies,
    get_vacancy_by_id,
    update_vacancy,
    delete_vacancy
)
from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required
from app.schemas.vacancies_schema import VacancySchemaBase, VacancyResponseSchema

router = APIRouter()

@router.post("/vacancies", tags=["Вакансии и должности"], description="Создать новую вакансию", response_model=VacancyResponseSchema)
def create_vacancy_route(
    form_data: VacancySchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return create_vacancy(form_data, session)

@router.get("/vacancies", tags=["Вакансии и должности"], description="Вывести все вакансии", response_model=list[VacancyResponseSchema])
def list_vacancies_route(session: Session = Depends(get_session)):
    return get_vacancies(session)

@router.get("/vacancies/{id}", tags=["Вакансии и должности"], description="Вывести вакансию по ID", response_model=VacancyResponseSchema)
def get_vacancy_route(id: int, session: Session = Depends(get_session)):
    return get_vacancy_by_id(id, session)

@router.put("/vacancies/{id}", tags=["Вакансии и должности"], description="Обновить вакансию", response_model=VacancyResponseSchema)
def update_vacancy_route(
    id: int,
    form_data: VacancySchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return update_vacancy(id, form_data, session)

@router.delete("/vacancies/{id}", tags=["Вакансии и должности"], description="Удалить вакансию")
def delete_vacancy_route(
    id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return delete_vacancy(id, session)

