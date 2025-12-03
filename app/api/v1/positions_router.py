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

@router.post("/positions", tags=["Вакансии и должности"], description="Создать новую должность", response_model=PositionResponseSchema)
def create_position_route(
    form_data: PositionSchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return create_position(form_data, session)

@router.get("/positions", tags=["Вакансии и должности"], description="Вывести все должности", response_model=list[PositionResponseSchema])
def list_positions_route(session: Session = Depends(get_session)):
    return get_positions(session)

@router.get("/positions/{id_pos}", tags=["Вакансии и должности"], description="Вывести должность по ID", response_model=PositionResponseSchema)
def get_position_route(id_pos: int, session: Session = Depends(get_session)):
    return get_position_by_id(id_pos, session)

@router.put("/positions/{id_pos}", tags=["Вакансии и должности"], description="Обновить должность", response_model=PositionResponseSchema)
def update_position_route(
    id_pos: int,
    form_data: PositionSchemaBase,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return update_position(id_pos, form_data, session)

@router.delete("/positions/{id_pos}", tags=["Вакансии и должности"], description="Удалить должность")
def delete_position_route(
    id_pos: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(admin_or_hr_required)
):
    return delete_position(id_pos, session)

