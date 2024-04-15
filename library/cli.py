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
    create_employee,
    edit_employee,
    delete_employee,
    edit_tickets_by_employee_id,
    edit_tickets_by_ticket_no,
    new_issue,
    edit_issue,
    remove_issue,
    view_issues
)

def login():
    while True:
        sweep_up_shop()
        print("Welcome to Ticket Tracker")
        print("Please enter your employee ID to continue.")
        print("If you wish to exit, press enter.")
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
        sweep_up_shop()
        print(f"Welcome Admin: {employee_info.name}")
        print("What would you like to do today?")
        print("Please enter a number to continue")
        print("0. Logout")
        print("1. View/Resolve Open Tickets")
        print("2. Add/Edit Employees")
        print("3. Add/Edit Issues")
        choice = input("> ")
        if choice == "0":
            login()
        elif choice == "1":
            ticket_search(employee_info)
        elif choice == "2":
            edit_employees(employee_info)
        elif choice == "3":
            edit_issues(employee_info)
        else:
            error_screen("Invalid Input")

def user_home(employee_info):
    while True:
        sweep_up_shop()
        print(f"Welcome User: {employee_info.name}")
        print("What would you like to do today?")
        print("Please enter a number to continue")
        print("0. Logout")
        print("1. Create a New Ticket")
        print("2. View Open Tickets")
        choice = input("> ")
        if choice == "0":
            login()
        elif choice == "1":
            ticket_subcat_menu(employee_info)
        elif choice == "2":
            user_view_tickets(employee_info)
        else:
            error_screen("Invalid Input")

def ticket_search(employee_info):
    while True:
        sweep_up_shop()
        print("How would you like to locate a ticket?")
        print("0. Back")
        print("1. Search by Employee ID")
        print("2. Search by Ticket Number")
        print("3. View All Open Tickets")
        print("4. Open New Ticket")
        choice = input("> ")
        if choice == "0":
            admin_home(employee_info)
        elif choice == "1":
            edit_tickets_by_employee_id()
        elif choice == "2":
            edit_tickets_by_ticket_no()
        elif choice == "3":
            admin_view_all_tickets()
        elif choice == "4":
            ticket_subcat_menu(employee_info)
        else:
            error_screen("Invalid Input")

def edit_employees(employee_info):
    while True:
        sweep_up_shop()
        print("What would you like to change today?")
        print("0. Back")
        print("1. Add a New Employee")
        print("2. Edit Current Employee")
        print("3. Terminate Employee")
        choice = input("> ")
        if choice == "0":
            admin_home(employee_info)
        elif choice == "1":
            create_employee()
        elif choice == "2":
            edit_employee()
        elif choice == "3":
            delete_employee()
        else:
            error_screen("Invalid Input")

def edit_issues(employee_info):
    while True:
        sweep_up_shop()
        print("What would you like to do today?")
        print("0. Back")
        print("1. Create a New Issue")
        print("2. Edit an Issue")
        print("3. Delete an Issue")
        print("4. View Current Issues")
        choice = input("> ")
        if choice == "0":
            admin_home(employee_info)
        elif choice == "1":
            new_issue_subcat_menu(employee_info)
        elif choice == "2":
            edit_issue()
        elif choice == "3":
            remove_issue()
        elif choice == "4":
            view_issues()
        else:
            error_screen("Invalid Input")

def ticket_subcat_menu(employee_info):
    sweep_up_shop()
    print("What is the nature of your issue?")
    print("0. Back")
    print("1. Hardware")
    print("2. Software")
    print("3. Permissions")
    print("4. Other")
    choice = input("> ")
    subcat = None
    if choice == "0":
        if employee_info.access_level == "admin":
            admin_home(employee_info)
        elif employee_info.access_level == "user":
            user_home(employee_info)
        else:
            error_screen("An internal error occurred. Please try again later.")
    elif choice == "1":
        subcat = "hardware"
    elif choice == "2":
        subcat = "software"
    elif choice == "3":
        subcat = "permissions"
    elif choice == "4":
        subcat = "other"
    else:
        error_screen("Invalid Input")
    new_ticket(employee_info, subcat)

def new_issue_subcat_menu(employee_info):
    sweep_up_shop()
    print("Creating New Issue, Please Select an Option")
    print("1. Hardware Issue")
    print("2. Software Issue")
    print("3. Permissions Issues")
    print("4. Other")
    choice = input("> ")
    subcat = None
    if choice == "1":
        subcat = "hardware"
    elif choice == "2":
        subcat = "software"
    elif choice == "3":
        subcat = "permissions"
    elif choice == "4":
        subcat = "other"
    else:
        error_screen("Invalid Input")
    new_issue(employee_info, subcat)

if __name__ == "__main__":
    login()