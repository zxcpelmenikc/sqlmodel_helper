# API учета персонала, вакансий и штатного расписания

Проект разработан для управления персоналом организации и предоставления информации о работниках, должностях, отделениях и штатном расписании.


RESTful API для управления персоналом организации, построенное на FastAPI. Система предоставляет функционал для:

- Управления сотрудниками (прием, увольнение, переводы)
- Управления должностями и вакансиями
- Управления отделами
- Управления штатным расписанием
- Аутентификации и авторизации пользователей

- **FastAPI** 0.120.4 - современный веб-фреймворк для создания API
- **SQLModel** 0.0.27 - ORM на основе SQLAlchemy и Pydantic
- **PostgreSQL** - реляционная база данных
- **Alembic** 1.17.2 - миграции базы данных
- **Pydantic** 2.12.3 - валидация данных
- **JWT** (python-jose) - аутентификация через токены
- **Argon2** - хеширование паролей
- **FastAPI Pagination** - пагинация результатов

1. Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# База данных
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name

# JWT настройки
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Создайте базу данных PostgreSQL:
```sql
CREATE DATABASE your_db_name;
```

3. Примените миграции (если используются):
```bash
alembic upgrade head
```

4. Запустите приложение:
```bash
uvicorn app.main:app_v1 --reload
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

Документация API доступна по адресу: `http://127.0.0.1:8000/docs`

## 📁 Структура проекта

```
sqlmodel_helper-api_working/
├── alembic/                  # Миграции базы данных
├── app/
│   ├── api/
│   │   └── v1/              # API роутеры версии 1
│   │       ├── api_users_router.py      # Роутер для пользователей
│   │       ├── departments_router.py    # Роутер для отделов
│   │       ├── employee_router.py       # Роутер для сотрудников
│   │       ├── positions_router.py      # Роутер для должностей
│   │       └── staffing_table_router.py # Роутер для штатного расписания
│   ├── controllers/          # Бизнес-логика
│   │   ├── departments_controller.py
│   │   ├── employees_controller.py
│   │   ├── positions_controller.py
│   │   ├── staffing_table_controller.py
│   │   └── users_controller.py
│   ├── core/
│   │   └── security.py      # Аутентификация и авторизация
│   ├── db/
│   │   ├── database.py      # Настройка подключения к БД
│   │   └── session.py       # Управление сессиями
│   ├── models/              # SQLModel модели
│   │   ├── departments.py
│   │   ├── employees.py
│   │   ├── positions.py
│   │   ├── users.py
│   │   └── ...
│   ├── schemas/             # Pydantic схемы
│   │   ├── employees_chema.py
│   │   ├── positions_schema.py
│   │   └── user_schema.py
│   └── main.py              # Точка входа приложения
├── requirements.txt
└── README.md
```

## 🔌 API Эндпоинты

### Вход и регистрация

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| POST | `/api/v1/accounts/sign_up` | Регистрация нового пользователя | Нет |
| POST | `/api/v1/accounts/sign_up_as_admin` | Регистрация пользователя администратором | Да (Admin) |
| POST | `/api/v1/auth/login` | Вход в систему | Нет |
| POST | `/api/v1/auth/refresh` | Обновление токена доступа | Нет |
| GET | `/api/v1/users` | Получить список всех пользователей | Да (Admin) |

### Работники

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| POST | `/api/v1/add_employee` | Добавить работника/принять на работу | Да (Admin) |
| GET | `/api/v1/employees` | Вывести список всех работников | Нет |
| GET | `/api/v1/employees_by_department/{department_id}` | Вывести список работников по отделениям | Нет |
| PUT | `/api/v1/employee/{id}` | Изменить информацию о работнике | Да (Admin) |
| PUT | `/api/v1/employees_changed_position/{position_id}` | Перевод работника на новую должность | Да (Admin) |
| GET | `/api/v1/fired_employees` | Вывести список уволенных работников | Нет |

### Вакансии и должности

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| POST | `/api/v1/positions` | Создать новую должность | Да (Admin) |
| GET | `/api/v1/positions` | Вывести все должности | Нет |
| GET | `/api/v1/positions/{id_pos}` | Вывести должность по ID | Нет |
| PUT | `/api/v1/positions/{id_pos}` | Обновить должность | Да (Admin) |
| DELETE | `/api/v1/positions/{id_pos}` | Удалить должность | Да (Admin) |

### Отделы

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| GET | `/api/v1/departments` | Вывести все отделения | Нет |
| PUT | `/api/v1/department/{id_dep}` | Изменить данные отделения | Да (Admin) |

### Штатное расписание

| Метод | Эндпоинт | Описание | Требует авторизации |
|-------|----------|----------|---------------------|
| GET | `/api/v1/staffing_table` | Вывод расписания с названием должности и департамента | Нет |
| PUT | `/api/v1/staffing_table/{id}` | Изменение расписания | Да (Admin) |

## 🔐 Аутентификация

API использует JWT (JSON Web Tokens) для аутентификации. Для доступа к защищенным эндпоинтам необходимо:

1. Получить токен через `/api/v1/auth/login`
2. Использовать токен в заголовке запроса:
```
Authorization: Bearer <your_token>
```

### Роли пользователей

- **Обычный пользователь** (role_id=2) - базовый доступ
- **Администратор** (role_id=1) - полный доступ ко всем операциям

## 📖 Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/accounts/sign_up" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user123",
    "password": "securepassword"
  }'
```

### Вход в систему

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user123&password=securepassword"
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Добавление сотрудника (требует авторизации администратора)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/add_employee" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Иванович",
    "tab_number": 12345,
    "department_id": 1,
    "position_id": 1,
    "inn": "123456789012",
    "snils": "12345678901",
    "gender": "мужской",
    "birth_date": "1990-01-01",
    "birth_place": "Москва",
    "address": "ул. Примерная, д. 1",
    "education": "Высшее",
    "profession": "Инженер",
    "marital_status": "Женат",
    "hire_date": "2024-01-01",
    "dismissal_date": "",
    "is_active": true
  }'
```

### Получение списка сотрудников

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/employees?page=1&size=10" \
  -H "accept: application/json"
```

### Создание должности (требует авторизации администратора)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/positions" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name_position": "Старший разработчик",
    "code_position": "DEV-001"
  }'
```

### Получение всех должностей

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/positions" \
  -H "accept: application/json"
```

## 📊 Модели данных

### Employees (Сотрудники)
- `id` - Уникальный идентификатор
- `last_name` - Фамилия
- `first_name` - Имя
- `middle_name` - Отчество
- `tab_number` - Табельный номер
- `department_id` - ID отдела
- `position_id` - ID должности
- `inn` - ИНН
- `snils` - СНИЛС
- `gender` - Пол
- `birth_date` - Дата рождения
- `birth_place` - Место рождения
- `address` - Адрес
- `education` - Образование
- `profession` - Профессия
- `marital_status` - Семейное положение
- `hire_date` - Дата приема на работу
- `dismissal_date` - Дата увольнения
- `is_active` - Статус активности

### Positions (Должности)
- `id_pos` - Уникальный идентификатор
- `name_position` - Название должности
- `code_position` - Код должности

### Departments (Отделы)
- `id_dep` - Уникальный идентификатор
- `name_dep` - Название отдела
- `code_dep` - Код отдела

### Users (Пользователи)
- `id` - Уникальный идентификатор
- `username` - Имя пользователя
- `password` - Хешированный пароль
- `role_id` - ID роли (1 - администратор, 2 - обычный пользователь)

## 🔒 Безопасность

- Пароли хешируются с использованием Argon2
- JWT токены для аутентификации
- Ролевая модель доступа (RBAC)
- Валидация данных через Pydantic
- Защита от SQL-инъекций через SQLModel/SQLAlchemy

## 📝 Примечания

- Для операций создания, обновления и удаления требуется роль администратора
- Пустые строки в поле `dismissal_date` автоматически конвертируются в `null`
- При создании новых записей поле `id` автоматически исключается из payload
- API поддерживает пагинацию для списковых запросов

## 🐛 Обработка ошибок

API возвращает стандартные HTTP коды статуса:

- `200` - Успешный запрос
- `201` - Ресурс создан
- `400` - Неверный запрос
- `401` - Не авторизован
- `403` - Доступ запрещен (требуются права администратора)
- `404` - Ресурс не найден
- `422` - Ошибка валидации данных
- `500` - Внутренняя ошибка сервера

## 📚 Документация

Интерактивная документация API доступна по адресу:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 👥 Авторы
Перетолчин Е.А                                                          Pencil Corporation
Проект разработан для управления персоналом организации.


