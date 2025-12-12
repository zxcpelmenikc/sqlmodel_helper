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

@router.post("/vacancies", tags=["Вакансии и должности"], 
             description="Создать новую вакансию в системе. "
                        "**Доступ:** Только Администратор. "
                        "**Возможности:** Добавление новой вакансии с указанием отдела, должности, "
                        "количества мест и статуса (открыта/закрыта). "
                        "**Требуемые данные:** Все поля согласно схеме VacancySchemaBase.",
             response_model=VacancyResponseSchema,
             summary="Создать новую вакансию")
def create_vacancy_route(
    form_data: VacancySchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return create_vacancy(form_data, session)

@router.get("/vacancies", tags=["Вакансии и должности"], 
            description="Получить список всех вакансий в организации. "
                      "**Доступ:** Все пользователи (без авторизации). "
                      "**Возможности:** Просмотр всех открытых и закрытых вакансий с информацией об отделах, "
                      "должностях и статусах. "
                      "**Возвращает:** Список всех вакансий.",
            response_model=list[VacancyResponseSchema],
            summary="Получить список всех вакансий")
def list_vacancies_route(session: Session = Depends(get_session)):
    return get_vacancies(session)

@router.get("/vacancies/{id}", tags=["Вакансии и должности"], 
            description="Получить информацию о конкретной вакансии по её ID. "
                      "**Доступ:** Все пользователи (без авторизации). "
                      "**Возможности:** Просмотр детальной информации о вакансии. "
                      "**Параметры:** id (ID вакансии). "
                      "**Возвращает:** Полная информация о вакансии.",
            response_model=VacancyResponseSchema,
            summary="Получить вакансию по ID")
def get_vacancy_route(id: int, session: Session = Depends(get_session)):
    return get_vacancy_by_id(id, session)

@router.put("/vacancies/{id}", tags=["Вакансии и должности"], 
            description="Обновить информацию о вакансии. "
                      "**Доступ:** Только Администратор. "
                      "**Возможности:** Изменение данных вакансии (отдел, должность, количество мест, статус). "
                      "Можно использовать для закрытия вакансии (изменение статуса). "
                      "**Параметры:** id (ID вакансии), данные для обновления согласно схеме VacancySchemaBase.",
            response_model=VacancyResponseSchema,
            summary="Обновить вакансию")
def update_vacancy_route(
    id: int,
    form_data: VacancySchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return update_vacancy(id, form_data, session)

@router.delete("/vacancies/{id}", tags=["Вакансии и должности"], 
               description="Удалить вакансию из системы. "
                         "**Доступ:** Только Администратор. "
                         "**Возможности:** Полное удаление вакансии из базы данных. "
                         "**Параметры:** id (ID вакансии для удаления).",
               response_model=dict,
               summary="Удалить вакансию")
def delete_vacancy_route(
    id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return delete_vacancy(id, session)

