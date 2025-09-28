from models.employees import Employees
from sqlmodel import Session, select
from datetime import date 
from db.database import engine

def get_all_employees():
    with Session(engine) as session:
        statement = select(Employees)
        results = session.exec(statement)
        employees = results.all()
        return employees
    
def add_employees(id, first_name, last_name, middle_name, tab_number, inn, snils, gender, birth_date, birth_place, address, education, profession, marital_status, hire_date, dismissal_date, is_active):
    """
    Добавление нового сотрудника
    """
    with Session(engine) as session:
        employee = Employees(id=id, first_name=first_name, last_name=last_name, middle_name=middle_name, tab_number=tab_number, inn=inn, 
                             snils=snils, gender=gender, birth_date=birth_date, birth_place=birth_place, address=address, 
                             education=education, profession=profession, marital_status=marital_status, hire_date=hire_date, dismissal_date=dismissal_date, is_active=is_active)
        session.add(employee)
        session.commit()
        return True
