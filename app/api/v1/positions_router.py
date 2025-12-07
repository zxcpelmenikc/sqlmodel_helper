from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.controllers.positions_controller import (
    create_position,
    get_positions,
    get_position_by_id,
    update_position,
    delete_position
)
from app.models.users import Users
from app.core.security import admin_required, admin_or_hr_required
from app.schemas.positions_schema import PositionSchemaBase, PositionResponseSchema

router = APIRouter()

@router.post("/positions", tags=["Вакансии и должности"], 
             description="Создать новую должность в системе. "
                        "**Доступ:** Только Администратор. "
                        "**Возможности:** Добавление новой должности с названием и кодом должности. "
                        "Код должности должен соответствовать коду отдела (например, DEV-001 для отдела DEV). "
                        "**Требуемые данные:** name_position (название должности), code_position (код должности).",
             response_model=PositionResponseSchema)
def create_position_route(
    form_data: PositionSchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return create_position(form_data, session)

@router.get("/positions", tags=["Вакансии и должности"], 
            description="Получить список всех должностей в организации. "
                      "**Доступ:** Все пользователи (без авторизации). "
                      "**Возможности:** Просмотр всех доступных должностей с их названиями и кодами. "
                      "**Возвращает:** Список всех должностей.",
            response_model=list[PositionResponseSchema])
def list_positions_route(session: Session = Depends(get_session)):
    return get_positions(session)

@router.get("/positions/{id_pos}", tags=["Вакансии и должности"], 
            description="Получить информацию о конкретной должности по её ID. "
                      "**Доступ:** Все пользователи (без авторизации). "
                      "**Возможности:** Просмотр детальной информации о должности. "
                      "**Параметры:** id_pos (ID должности). "
                      "**Возвращает:** Полная информация о должности.",
            response_model=PositionResponseSchema)
def get_position_route(id_pos: int, session: Session = Depends(get_session)):
    return get_position_by_id(id_pos, session)

@router.put("/positions/{id_pos}", tags=["Вакансии и должности"], 
            description="Обновить информацию о должности. "
                      "**Доступ:** Только Администратор. "
                      "**Возможности:** Изменение названия или кода должности. "
                      "**Параметры:** id_pos (ID должности), данные для обновления согласно схеме PositionSchemaBase.",
            response_model=PositionResponseSchema)
def update_position_route(
    id_pos: int,
    form_data: PositionSchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return update_position(id_pos, form_data, session)

@router.delete("/positions/{id_pos}", tags=["Вакансии и должности"], 
               description="Удалить должность из системы. "
                         "**Доступ:** Только Администратор. "
                         "**Возможности:** Удаление должности. Внимание: удаление возможно только если "
                         "на этой должности нет сотрудников. "
                         "**Параметры:** id_pos (ID должности для удаления).",
               response_model=dict)
def delete_position_route(
    id_pos: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_required)
):
    return delete_position(id_pos, session)

