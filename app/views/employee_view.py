from db.database import *
from models.employees import Employees
from sqlmodel import Session, select
from datetime import datetime

def _parse_date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    # ожидаемый формат ввода: ДД-MM-YYYY, можно добавить другие форматы при необходимости
    return datetime.strptime(s, "%d-%m-%Y").date()

def print_all_employees(employees):
    for employee in employees:
        print(f"ID: {employee.id}, Name: {employee.last_name}, Position: {employee.first_name}, Tab Number: {employee.tab_number}, Inn: {employee.inn}, Snils: {employee.snils}")

def add_employee():
    """
    Добавление сотрудника
    """
    id = int(input("введи ID: "))
    last_name = input("Фамилия: ")
    first_name = input("Имя: ")
    middle_name = input("Отчество: ")
    tab_number = int(input("Табельный номер: "))
    inn = input("ИНН: ")
    snils = input("СНИЛС: ")
    gender = input("Пол: ")
    birth_date = _parse_date(input("Дата рождения (ДД-MM-YYYY): "))
    birth_place = input("Место рождения: ")
    address = input("Адрес: ")
    education = input("Образование: ")
    profession = input("Профессия: ")
    marital_status = input("Семейное положение: ")
    hire_date = _parse_date(input("Дата приема (ДД-MM-YYYY): "))
    dismissal_date = _parse_date(input("Дата увольнения (оставьте пустым если нет): "))
    is_active = True if input("Активен? (y/n): ").lower().startswith("y") else False
    
    return id, first_name, last_name, middle_name, tab_number, inn, snils, gender, birth_date, birth_place, address, education, profession, marital_status, hire_date, dismissal_date, is_active