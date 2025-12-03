from fastapi_pagination import add_pagination
from app.db.database import *
from app.controllers.employees_controller import get_employees
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.api.v1.employee_router import router
from app.api.v1.api_users_router import router as user_router
from app.core.security import oauth2_scheme
from typing import Annotated
from app.api.v1.departments_router import router as dept_router
from app.api.v1.staffing_table_router import router as staffing_router
from app.api.v1.positions_router import router as positions_router
from app.api.v1.vacancies_router import router as vacancies_router


@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()
    yield
    close_db()
app_v1 = FastAPI(lifespan=on_startup, title="API учета персонала, вакансий и штатного расписания", description= "Проект разработан для управления персоналом организации и предоставления информации о работниках, должностях, отделениях и штатном расписании", version="1.0.0")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

app_v1.include_router(user_router, prefix="/api/v1")
app_v1.include_router(router, prefix="/api/v1")
app_v1.include_router(dept_router, prefix="/api/v1")
app_v1.include_router(staffing_router, prefix="/api/v1")
app_v1.include_router(positions_router, prefix="/api/v1")
app_v1.include_router(vacancies_router, prefix="/api/v1")

add_pagination(app_v1)

