from models.employee import Employee
from models.issue import Issue
from helpers import (
    sweep_up_shop,
    exit_program,
    error_screen,
    new_ticket,
    user_view_tickets,
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
                permissions = employee[3]
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
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        else:
            error_screen("Choice does not exist. Please choose from list")

def admin_menu(employee_info):
    sweep_up_shop()
    print(f"Welcome Admin: {employee_info[1]}")
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
    print(f"Welcome User: {employee_info[1]}")
    print("What would you like to do today?")
    print("Please enter a number to continue")
    print("0. Logout")
    print("1. Create a New Ticket")
    print("2. View Open Tickets")

if __name__ == "__main__":
    login()