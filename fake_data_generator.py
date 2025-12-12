"""
Модуль для генерации тестовых данных с использованием Faker.
"""
import random
from datetime import date, timedelta
from faker import Faker
from faker.providers import BaseProvider
from argon2 import PasswordHasher
from sqlmodel import Session, select
from app.db.database import engine, init_db
from app.models.roles import Roles
from app.models.departments import Departments
from app.models.positions import Positions
from app.models.users import Users
from app.models.employees import Employees
from app.models.staffing_table import Staffing_table
from app.models.vacancies import Vacancies

# Инициализация Faker с русской локалью
fake = Faker('ru_RU')
ph = PasswordHasher()

class RussianProvider(BaseProvider):
    """Провайдер для генерации российских данных"""
    def inn(self):
        """Генерирует ИНН (12 цифр)"""
        return ''.join([str(random.randint(0, 9)) for _ in range(12)])
    
    def snils(self):
        """Генерирует СНИЛС (11 цифр в формате XXX-XXX-XXX XX)"""
        snils_digits = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        return f"{snils_digits[:3]}-{snils_digits[3:6]}-{snils_digits[6:9]} {snils_digits[9:11]}"

fake.add_provider(RussianProvider)

def generate_roles(session: Session):
    """Генерация ролей"""
    print("Генерация ролей...")
    roles_data = [
        {"name": "Администратор", "description": "Администратор системы. Полный доступ ко всем функциям."},
        {"name": "HR-менеджер", "description": "HR-менеджер. Управление сотрудниками."},
        {"name": "Пользователь", "description": "Обычный пользователь. Базовый доступ к системе."},
    ]
    
    for role_data in roles_data:
        existing = session.exec(select(Roles).where(Roles.name == role_data["name"])).first()
        if not existing:
            role = Roles(**role_data)
            session.add(role)
    
    session.commit()
    print("Роли созданы")
    return session.exec(select(Roles)).all()


def generate_departments(session: Session, count: int = 5):
    """Генерация отделов"""
    print(f"Генерация {count} отделов...")
    departments = []
    
    department_names = [
        ("Отдел разработки", "DEV"),
        ("Отдел тестирования", "QA"),
        ("Отдел продаж", "SALES"),
        ("Отдел маркетинга", "MKT"),
        ("HR отдел", "HR"),
        ("Финансовый отдел", "FIN"),
        ("Отдел поддержки", "SUPPORT"),
        ("Отдел безопасности", "SEC"),
    ]
    
    existing_departments = session.exec(select(Departments)).all()
    if existing_departments:
        print(f"Найдено {len(existing_departments)} существующих отделов")
        return existing_departments
    
    for i in range(count):
        if i < len(department_names):
            name_dep, code_dep = department_names[i]
        else:
            name_dep = fake.company()
            code_dep = fake.lexify(text='???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        department = Departments(
            name_dep=name_dep,
            code_dep=code_dep
        )
        session.add(department)
        departments.append(department)
    
    session.commit()
    for dept in departments:
        session.refresh(dept)
    print(f"Создано {len(departments)} отделов")
    return session.exec(select(Departments)).all()


def generate_positions(session: Session, count: int = 10):
    """Генерация должностей"""
    print(f"Генерация {count} должностей...")
    positions = []
    
    position_names = [
        ("Разработчик", "DEV-001"),
        ("Старший разработчик", "DEV-002"),
        ("Тестировщик", "QA-001"),
        ("Старший тестировщик", "QA-002"),
        ("Менеджер по продажам", "SALES-001"),
        ("Директор по продажам", "SALES-002"),
        ("Маркетолог", "MKT-001"),
        ("HR-менеджер", "HR-001"),
        ("Бухгалтер", "FIN-001"),
        ("Главный бухгалтер", "FIN-002"),
        ("Специалист поддержки", "SUPPORT-001"),
        ("Инженер безопасности", "SEC-001"),
    ]
    
    existing_positions = session.exec(select(Positions)).all()
    if existing_positions:
        print(f"Найдено {len(existing_positions)} существующих должностей")
        return existing_positions
    
    for i in range(count):
        if i < len(position_names):
            name_position, code_position = position_names[i]
        else:
            name_position = fake.job()
            code_position = fake.lexify(text='???-###', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        position = Positions(
            name_position=name_position,
            code_position=code_position
        )
        session.add(position)
        positions.append(position)
    
    session.commit()
    for pos in positions:
        session.refresh(pos)
    print(f"Создано {len(positions)} должностей")
    return session.exec(select(Positions)).all()


def generate_users(session: Session, roles: list, count: int = 10):
    """Генерация пользователей"""
    print(f"Генерация {count} пользователей...")
    users = []
    
    # Первый пользователь - админ (если еще не существует)
    admin_role = next((r for r in roles if r.name == "Администратор"), None)
    if admin_role:
        existing_admin = session.exec(select(Users).where(Users.username == "admin")).first()
        if not existing_admin:
            admin_user = Users(
                username="admin",
                password=ph.hash("admin123"),
                role_id=admin_role.id
            )
            session.add(admin_user)
            users.append(admin_user)
            count -= 1
        else:
            users.append(existing_admin)
            count -= 1
    
    # Генерация остальных пользователей
    user_role = next((r for r in roles if r.name == "Пользователь"), None)
    if not user_role:
        user_role = roles[-1] if roles else None
    
    for i in range(count):
        username = fake.user_name() + str(random.randint(100, 999))
        # Проверяем уникальность
        existing = session.exec(select(Users).where(Users.username == username)).first()
        if existing:
            continue
        
        password = ph.hash("password123")  # Все имеют одинаковый пароль для тестирования
        
        user = Users(
            username=username,
            password=password,
            role_id=user_role.id if user_role else roles[0].id
        )
        session.add(user)
        users.append(user)
    
    session.commit()
    for user in users:
        session.refresh(user)
    print(f"Создано {len(users)} пользователей")
    return session.exec(select(Users)).all()


def generate_employees(session: Session, departments: list, positions: list, count: int = 10):
    """Генерация сотрудников"""
    print(f"Генерация {count} сотрудников...")
    employees = []
    
    # Варианты для генерации
    genders = ["мужской", "женский"]
    educations = ["Высшее", "Среднее специальное", "Среднее", "Неполное высшее"]
    professions = ["Инженер", "Бухгалтер", "Менеджер", "Программист", "Дизайнер", "Аналитик", "Юрист", "Экономист"]
    marital_statuses = ["Женат", "Замужем", "Холост", "Не замужем", "Разведен", "Разведена"]
    
    # Получаем максимальный табельный номер для генерации уникальных
    existing_employees = session.exec(select(Employees.tab_number)).all()
    max_tab = max([num for num in existing_employees if num is not None], default=0)
    
    for i in range(count):
        # Генерируем имя и фамилию
        gender = random.choice(genders)
        if gender == "мужской":
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
            middle_name = fake.middle_name_male()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
            middle_name = fake.middle_name_female()
        
        # Генерируем дату рождения (от 20 до 65 лет)
        birth_date = fake.date_of_birth(minimum_age=20, maximum_age=65)
        
        # Генерируем дату приема на работу (не раньше даты рождения + 18 лет, не позже сегодня)
        min_hire_date = birth_date + timedelta(days=18*365)
        hire_date = fake.date_between(start_date=min_hire_date, end_date='today')
        
        # Генерируем ИНН и СНИЛС
        inn = fake.inn()
        snils = fake.snils()
        
        # Случайно выбираем отдел
        department = random.choice(departments)
        
        # Выбираем должность, которая соответствует отделу по коду
        # Например: отдел "DEV" -> должности "DEV-001", "DEV-002"
        matching_positions = [pos for pos in positions if pos.code_position.startswith(department.code_dep)]
        
        if not matching_positions:
            # Если нет подходящих должностей, выбираем любую (на случай ошибки в данных)
            print(f"Предупреждение: Для отдела {department.name_dep} (код: {department.code_dep}) не найдено подходящих должностей!")
            position = random.choice(positions)
        else:
            position = random.choice(matching_positions)
        
        # Генерируем табельный номер (уникальный)
        max_tab += 1
        tab_number = max_tab
        
        # Определяем, активен ли сотрудник (75% активных)
        is_active = random.choice([True, True, True, False])
        dismissal_date = None if is_active else fake.date_between(start_date=hire_date, end_date='today')
        
        employee = Employees(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            tab_number=tab_number,
            department_id=department.id_dep,
            position_id=position.id_pos,
            inn=inn,
            snils=snils,
            gender=gender,
            birth_date=birth_date,
            birth_place=fake.city(),
            address=fake.address(),
            education=random.choice(educations),
            profession=random.choice(professions),
            marital_status=random.choice(marital_statuses),
            hire_date=hire_date,
            dismissal_date=dismissal_date,
            is_active=is_active
        )
        session.add(employee)
        employees.append(employee)
    
    session.commit()
    for employee in employees:
        session.refresh(employee)
    print(f"Создано {len(employees)} сотрудников")
    return session.exec(select(Employees)).all()


def generate_staffing_table(session: Session, departments: list, positions: list, employees: list, count: int = 10):
    """Генерация штатного расписания (максимум count записей)"""
    print(f"Генерация штатного расписания (максимум {count} записей)...")
    staffing_records = []
    
    # Проверяем существующие записи
    existing_staffing = session.exec(select(Staffing_table)).all()
    if existing_staffing:
        print(f"Найдено {len(existing_staffing)} существующих записей штатного расписания")
        return existing_staffing
    
    # Создаем комбинации отделов и должностей только с совпадающими кодами
    # Например: DEV (отдел) с DEV-001, DEV-002 (должности)
    all_combinations = []
    for dept in departments:
        for pos in positions:
            # Проверяем, что код должности начинается с кода отдела
            # Например: код отдела "DEV" и код должности "DEV-001"
            if pos.code_position.startswith(dept.code_dep):
                all_combinations.append((dept, pos))
    
    # Если нет подходящих комбинаций, выводим предупреждение
    if not all_combinations:
        print("Предупреждение: Не найдено комбинаций отделов и должностей с совпадающими кодами!")
        return []
    
    # Если комбинаций меньше count, создаем дополнительные комбинации
    # Для этого используем существующие отделы и создаем для них дополнительные должности
    if len(all_combinations) < count:
        needed = count - len(all_combinations)
        created_positions = []
        
        # Создаем дополнительные должности для существующих отделов
        for i in range(needed):
            # Выбираем случайный отдел
            dept = random.choice(departments)
            
            # Находим максимальный номер должности для этого отдела
            existing_positions_for_dept = [pos for pos in positions if pos.code_position.startswith(dept.code_dep)]
            max_num = 0
            for pos in existing_positions_for_dept:
                # Извлекаем номер из кода (например, "DEV-002" -> 2)
                try:
                    num_part = pos.code_position.split('-')[1] if '-' in pos.code_position else ''
                    num = int(num_part) if num_part.isdigit() else 0
                    max_num = max(max_num, num)
                except:
                    pass
            
            # Создаем новую должность с увеличенным номером
            new_num = max_num + 1
            new_code = f"{dept.code_dep}-{new_num:03d}"
            new_name = f"{fake.job()} ({dept.name_dep})"
            
            # Проверяем, что такой должности еще нет
            existing_pos = session.exec(select(Positions).where(Positions.code_position == new_code)).first()
            if not existing_pos:
                new_position = Positions(
                    name_position=new_name,
                    code_position=new_code
                )
                session.add(new_position)
                created_positions.append(new_position)
                all_combinations.append((dept, new_position))
            else:
                all_combinations.append((dept, existing_pos))
        
        if created_positions:
            session.commit()
            for pos in created_positions:
                session.refresh(pos)
            print(f"Создано {len(created_positions)} дополнительных должностей для достижения {count} записей")
    
    # Ограничиваем количество комбинаций до count
    if len(all_combinations) > count:
        # Выбираем случайные комбинации
        selected_combinations = random.sample(all_combinations, count)
    else:
        selected_combinations = all_combinations[:count]
    
    # Для каждой выбранной комбинации создаем запись в штатном расписании
    for department, position in selected_combinations:
            # Подсчитываем количество сотрудников с этой комбинацией
            employees_count = len([
                emp for emp in employees 
                if emp.department_id == department.id_dep and emp.position_id == position.id_pos
            ])
            
            # Генерируем зарплату в зависимости от должности
            # Базовые зарплаты для разных должностей
            base_salaries = {
                "Разработчик": 80000,
                "Старший разработчик": 120000,
                "Тестировщик": 60000,
                "Старший тестировщик": 90000,
                "Менеджер по продажам": 70000,
                "Директор по продажам": 150000,
                "Маркетолог": 65000,
                "HR-менеджер": 75000,
                "Бухгалтер": 60000,
                "Главный бухгалтер": 100000,
                "Специалист поддержки": 50000,
                "Инженер безопасности": 90000,
            }
            
            # Определяем базовую зарплату
            base_salary = base_salaries.get(position.name_position, 60000)
            # Добавляем случайное отклонение ±20%
            salary = round(base_salary * random.uniform(0.8, 1.2), 2)
            
            # Надбавки (10-30% от оклада)
            nadbavki = round(salary * random.uniform(0.1, 0.3), 2)
            
            # Общая зарплата
            total_salary = round(salary + nadbavki, 2)
            
            # Количество единиц (текущее количество сотрудников)
            units = employees_count
            
            # Количество единиц, которые нужны (обычно больше текущего)
            units_needed = max(units, random.randint(1, 5))
            
            # Детали (опционально)
            details = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
            
            staffing_record = Staffing_table(
                dep_id=department.id_dep,
                pos_id=position.id_pos,
                units=units,
                units_needed=units_needed,
                salary=salary,
                nadbavki=nadbavki,
                total_salary=total_salary,
                details=details
            )
            session.add(staffing_record)
            staffing_records.append(staffing_record)
    
    session.commit()
    for record in staffing_records:
        session.refresh(record)
    print(f"Создано {len(staffing_records)} записей штатного расписания")
    return session.exec(select(Staffing_table)).all()


def generate_vacancies(session: Session, departments: list, positions: list, count: int = 5):
    """Генерация вакансий"""
    print(f"Генерация {count} вакансий...")
    vacancies = []
    
    # Проверяем существующие вакансии
    existing_vacancies = session.exec(select(Vacancies)).all()
    if existing_vacancies:
        print(f"Найдено {len(existing_vacancies)} существующих вакансий")
        return existing_vacancies
    
    # Статусы вакансий
    statuses = ["open", "closed"]
    
    # Создаем комбинации отделов и должностей с совпадающими кодами
    all_combinations = []
    for dept in departments:
        for pos in positions:
            # Проверяем, что код должности начинается с кода отдела
            if pos.code_position.startswith(dept.code_dep):
                all_combinations.append((dept, pos))
    
    # Если нет подходящих комбинаций, используем любые
    if not all_combinations:
        print("Предупреждение: Не найдено комбинаций отделов и должностей с совпадающими кодами! Используются любые комбинации.")
        for dept in departments:
            for pos in positions:
                all_combinations.append((dept, pos))
    
    # Ограничиваем количество комбинаций до count
    if len(all_combinations) > count:
        # Выбираем случайные комбинации
        selected_combinations = random.sample(all_combinations, count)
    else:
        # Если комбинаций меньше count, повторяем некоторые
        selected_combinations = all_combinations[:count]
        while len(selected_combinations) < count:
            selected_combinations.append(random.choice(all_combinations))
    
    # Для каждой выбранной комбинации создаем вакансию
    for department, position in selected_combinations:
        # Генерируем количество единиц (от 1 до 5)
        units = random.randint(1, 5)
        
        # Выбираем случайный статус (70% открытых, 30% закрытых)
        status = random.choices(statuses, weights=[70, 30])[0]
        
        vacancy = Vacancies(
            dep_id=department.id_dep,
            pos_id=position.id_pos,
            units=units,
            status=status
        )
        session.add(vacancy)
        vacancies.append(vacancy)
    
    session.commit()
    for vacancy in vacancies:
        session.refresh(vacancy)
    print(f"Создано {len(vacancies)} вакансий")
    return session.exec(select(Vacancies)).all()


def update_units_in_staffing_table(session: Session):
    """
    Подсчитывает количество работников с теми же dep_id и pos_id для каждой записи
    в staffing_table и обновляет поле units.
    
    Args:
        session: Сессия базы данных
        
    Returns:
        Список обновленных записей Staffing_table
    """
    try:
        # Получаем все записи staffing_table
        stmt = select(Staffing_table)
        all_staffing = session.exec(stmt).all()
        
        updated_records = []
        
        for staffing_record in all_staffing:
            dep_id = staffing_record.dep_id
            pos_id = staffing_record.pos_id
            
            # Если dep_id или pos_id не указаны, устанавливаем units = 0
            if dep_id is None or pos_id is None:
                staffing_record.units = 0
                session.add(staffing_record)
                updated_records.append(staffing_record)
                continue
            
            # Подсчитываем количество работников с теми же department_id и position_id
            stmt_employees = select(Employees).where(
                Employees.department_id == dep_id,
                Employees.position_id == pos_id
            )
            employees = session.exec(stmt_employees).all()
            count = len(employees)
            
            # Обновляем поле units
            staffing_record.units = count
            session.add(staffing_record)
            updated_records.append(staffing_record)
        
        session.commit()
        
        # Обновляем объекты в сессии
        for record in updated_records:
            session.refresh(record)
        
        return updated_records
        
    except Exception as e:
        session.rollback()
        raise Exception(f"Ошибка при обновлении units: {str(e)}")


def main():
    """Основная функция генерации данных"""
    print("=" * 50)
    print("Генерация тестовых данных с помощью Faker")
    print("=" * 50)
    
    # Инициализация БД
    init_db()
    
    with Session(engine) as session:
        try:
            # Генерация базовых данных
            roles = generate_roles(session)
            departments = generate_departments(session, count=5)
            positions = generate_positions(session, count=10)
            users = generate_users(session, roles, count=10)
            employees = generate_employees(session, departments, positions, count=50)
            staffing_table = generate_staffing_table(session, departments, positions, employees, count = 10)
            vacancies = generate_vacancies(session, departments, positions, count=5)
            
            # Обновляем units в штатном расписании на основе реального количества сотрудников
            print("\nОбновление количества единиц (units) в штатном расписании...")
            updated_staffing = update_units_in_staffing_table(session)
            print(f"Обновлено {len(updated_staffing)} записей штатного расписания")
            
            print("\n" + "=" * 50)
            print("Генерация данных завершена успешно!")
            print("=" * 50)
            print(f"\nСоздано:")
            print(f"  - Ролей: {len(roles)}")
            print(f"  - Отделов: {len(departments)}")
            print(f"  - Должностей: {len(positions)}")
            print(f"  - Пользователей: {len(users)}")
            print(f"  - Сотрудников: {len(employees)}")
            print(f"  - Записей штатного расписания: {len(staffing_table)}")
            print(f"  - Вакансий: {len(vacancies)}")
            print(f"\nДанные для входа:")
            print(f"  Администратор:")
            print(f"    Username: admin")
            print(f"    Password: admin123")
            print(f"\n  Остальные пользователи:")
            print(f"    Username: <любой сгенерированный username>")
            print(f"    Password: password123")
            print(f"\n  Примеры сгенерированных пользователей:")
            all_users = session.exec(select(Users)).all()
            example_count = 0
            for user in all_users:
                if user.username != "admin" and example_count < 5:
                    print(f"    - Username: {user.username}")
                    print(f"      Password: password123")
                    example_count += 1
            print("\nВсе пользователи (кроме админа) имеют одинаковый пароль: password123")
            print("=" * 50)
            
        except Exception as e:
            session.rollback()
            print(f"\nОшибка при генерации данных: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    main()
