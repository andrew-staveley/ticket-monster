from models.employee import Employee
from models.issue import Issue
from models.ticket import Ticket
from helpers import (
    sweep_up_shop,
    exit_program,
    error_screen,
    new_ticket,
    user_view_tickets,
    admin_view_all_tickets,
    admin_edit_ticket,
    create_employee,
    edit_employee,
    delete_employee,
    edit_tickets_by_employee_id,
    edit_tickets_by_ticket_no,

)
def login():
    while True:
        login_menu()
        employee_login = input("> ")
        if employee_login == "":
            exit_program()
        else:
            employee = Employee.find_by_employee_id(int(employee_login))
            permissions = None
            if employee:
                permissions = employee.access_level
        if permissions == "admin":
            admin_home(employee)
        elif permissions == "user":
            user_home(employee)
        elif permissions == None:
            error_screen("Employee Login doesn't exist. Please contact system administrator.")
        else:
            error_screen("A fatal error occured, please try again later.")

def login_menu():
    sweep_up_shop()
    print("Welcome to Ticket Tracker")
    print("Please enter your employee ID to continue.")
    print("If you wish to exit, press enter.")

def admin_home(employee_info):
    while True:
        admin_menu(employee_info)
        choice = input("> ")
        if choice == "0":
            login()
        elif choice == "1":
            admin_ticket_search(employee_info)
        elif choice == "2":
            edit_employee_database()
        elif choice == "3":
            pass
        else:
            error_screen("Choice does not exist. Please choose from list")

def admin_menu(employee_info):
    sweep_up_shop()
    print(f"Welcome Admin: {employee_info.name}")
    print("What would you like to do today?")
    print("Please enter a number to continue")
    print("0. Logout")
    print("1. View/Resolve Open Tickets")
    print("2. Add/Edit Employees")
    print("3. Add/Edit Issues")

def user_home(employee_info):
    while True:
        user_menu(employee_info)
        choice = input("> ")
        if choice == "0":
            login()
        elif choice == "1":
            new_ticket(employee_info)
        elif choice == "2":
            user_view_tickets(employee_info)
        else:
            error_screen("Choice does not exist. Please choose from list.")


def user_menu(employee_info):
    sweep_up_shop()
    print(f"Welcome User: {employee_info.name}")
    print("What would you like to do today?")
    print("Please enter a number to continue")
    print("0. Logout")
    print("1. Create a New Ticket")
    print("2. View Open Tickets")

def admin_ticket_search(employee_info):
        admin_ticket_search_menu()
        choice = input("> ")
        if choice == "0":
            pass
        elif choice == "1":
            edit_tickets_by_employee_id()
        elif choice == "2":
            edit_tickets_by_ticket_no()
        elif choice == "3":
            admin_view_all_tickets()
        elif choice == "4":
            new_ticket(employee_info)
        else:
            error_screen("Invalid Input")

def admin_ticket_search_menu():
    sweep_up_shop()
    print("How would you like to locate a ticket?")
    print("0. Back")
    print("1. Search by Employee ID")
    print("2. Search by Ticket Number")
    print("3. View All Open Tickets")
    print("4. Open New Ticket")

def edit_employee_database():
    sweep_up_shop()
    edit_employee_database_menu()
    choice = input("> ")
    if choice == "0":
        pass
    elif choice == "1":
        create_employee()
    elif choice == "2":
        edit_employee()
    elif choice == "3":
        delete_employee()
    else:
        error_screen("Invalid Selection")

def edit_employee_database_menu():
    print("What would you like to change today?")
    print("0. Back")
    print("1. Add a New Employee")
    print("2. Edit Current Employee")
    print("3. Terminate Employee")

if __name__ == "__main__":
    login()

