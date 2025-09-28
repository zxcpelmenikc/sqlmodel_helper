from db.database import init_db
from controllers.employees_controller import add_employees, get_all_employees
from views.employee_view import add_employee, print_all_employees


from registration import reg
def main_menu():
    if not reg():
        return
    init_db()
    while True:
        print("\n--- Меню ---")
        print("1. Добавить сотрудника")
        print("2. Показать всех сотрудников")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            data = add_employee()
            add_employees(*data)
            print("Сотрудник добавлен.")
        elif choice == "2":
            employees = get_all_employees()
            print_all_employees(employees)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()


