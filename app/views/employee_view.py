from db.database import *
from models.employees import Employees
from sqlmodel import Session, select

def print_all_employees(employees):
    for employee in employees:
        print(f"ID: {employee.id}, Name: {employee.last_name}, Position: {employee.first_name}, Tab Number: {employee.tab_number}, Inn: {employee.inn}, Snils: {employee.snils}")

def add_employee():
    """
    Добавление сотрудника
    """
    id = int(input("введи ID: "))
    first_name = input("введи имя: ")
    last_name = input("введи фамилию: ")
    middle_name = input("введи отчество: ")
    tab_number = int(input("введи номер: "))
    inn = input("введи инн: ")
    snils = input("введи снилс: ")
    gender = input("введите пол: ")
    birth_date = input("введите дату рождения: ")
    birth_place = input("введите место рождения: ")
    address = input("введите адрес: ")
    education = input("введите образование: ")
    profession = input("введите профессию: ")
    marital_status = input("введите семейное положение: ")
    hire_date = input("введите дату приема на работу: ")
    dismissal_date = input("введите дату увольнения: ")
    is_active = input("введите активен ли сотрудник (True/False): ") == 'True'
    
    
    return id, first_name, last_name, middle_name, tab_number, inn, snils, gender, birth_date, birth_place, address, education, profession, marital_status, hire_date, dismissal_date, is_active