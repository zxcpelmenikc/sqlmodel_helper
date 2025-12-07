from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page
from sqlmodel import Session

from app.controllers.users_controller import login, refresh_access_token, get_users, admin_registration, registration, hr_registration
from app.core.security import get_current_user, admin_required, admin_or_hr_required
from app.db.session import get_session
from app.models.users import Users
from app.schemas.user_schema import UserSchema, UserSchemaCreateAsAdmin, UserSchemaCreate as USC

router = APIRouter()

@router.post("/accounts/sign_up_as_admin", tags=["Вход и регистрация"], 
             description="Зарегистрировать нового пользователя с правами администратора. "
                        "**Доступ:** Только Администратор. "
                        "**Возможности:** Создание нового пользователя с назначением роли администратора. "
                        "Только существующий администратор может создавать других администраторов. "
                        "**Требуемые данные:** username, password, role_id (ID роли администратора).",
             response_model=Users)
def sign_up_as_admin_route(
    form_data: UserSchemaCreateAsAdmin = Depends(UserSchemaCreateAsAdmin.as_form),
    user: Users = Depends(admin_required),
    session: Session = Depends(get_session)
):
    return admin_registration(form_data, user, session)

@router.post("/accounts/sign_up_as_hr", tags=["Вход и регистрация"], 
             description="Зарегистрировать нового пользователя с правами HR-менеджера. "
                        "**Доступ:** Все (без авторизации). "
                        "**Возможности:** Самостоятельная регистрация пользователя с ролью HR-менеджера. "
                        "Этот эндпоинт доступен без авторизации для упрощения процесса регистрации HR-специалистов. "
                        "**Требуемые данные:** username, password.",
             response_model=Users)
def sign_up_as_hr_route(
    form_data: USC = Depends(USC.as_form),
    session: Session = Depends(get_session)
):
    return hr_registration(form_data, session)

@router.post("/accounts/sign_up", tags=["Вход и регистрация"], 
             description="Зарегистрировать нового пользователя (обычный пользователь). "
                        "**Доступ:** Все (без авторизации). "
                        "**Возможности:** Самостоятельная регистрация нового пользователя с ролью обычного пользователя. "
                        "После регистрации пользователь получает базовый доступ к системе. "
                        "**Требуемые данные:** username, password.",
             response_model=Users)
def sign_up(form_data: UserSchema=Depends(USC.as_form),session:Session=Depends(get_session)):
    return registration(form_data, session)

@router.post("/auth/login", tags=["Вход и регистрация"], 
             description="Войти в систему (аутентификация). "
                        "**Доступ:** Все (без авторизации). "
                        "**Возможности:** Получение JWT токена доступа для работы с защищенными эндпоинтами. "
                        "Токен необходимо использовать в заголовке Authorization: Bearer <token> для доступа к защищенным ресурсам. "
                        "**Требуемые данные:** username, password. "
                        "**Возвращает:** access_token (токен доступа), token_type (тип токена - bearer).",
             response_model=dict)
def login_route(form_data: UserSchema=Depends(UserSchema.as_form),session:Session=Depends(get_session)):
    return login(form_data,session)

@router.post("/auth/refresh", tags=["Вход и регистрация"], 
             description="Обновить токен доступа. "
                        "**Доступ:** Все (без авторизации). "
                        "**Возможности:** Получение нового токена доступа по refresh токену без повторного ввода логина и пароля. "
                        "Используется для продления сессии пользователя. "
                        "**Требуемые данные:** refresh_token (refresh токен). "
                        "**Возвращает:** Новый access_token.",
             response_model=dict)
def refresh_token_route(refresh_token:str):
    return refresh_access_token(refresh_token)

@router.get("/users", tags=["Вход и регистрация"], 
            description="Получить список всех пользователей системы. "
                      "**Доступ:** Администратор, HR-менеджер. "
                      "**Возможности:** Просмотр всех зарегистрированных пользователей с их ролями. "
                      "Результаты возвращаются с пагинацией. "
                      "**Параметры:** page (номер страницы), size (размер страницы). "
                      "**Возвращает:** Список пользователей с информацией о username и role_id.",
            response_model=Page[Users])
def get_users_route(current_user: Users = Depends(admin_or_hr_required),session: Session=Depends(get_session)):
        return  get_users(current_user,session)