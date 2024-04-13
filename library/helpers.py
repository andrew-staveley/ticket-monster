from models.employee import Employee
from models.issue import Issue
from models.ticket import Ticket
import os
import platform
import random
import datetime

def sweep_up_shop():
    clr = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(clr)

def exit_program():
    sweep_up_shop()
    print("Goodbye!")
    exit()

def error_screen(error_info):
    sweep_up_shop()
    print("There was an error processing your request.")
    print("")
    print(error_info)
    print("")
    print("Press Enter to Continue")
    print("")
    input(">>> ")

def success_screen(success_info):
    sweep_up_shop()
    print("Success! Your request was completed!")
    print("")
    print(success_info)
    print("")
    print("Press Enter to Continue")
    print("")
    input(">>> ")

# Generates and validates new standardized employee ID numbers
def en_generator():
    new_employee_number = random.randrange(1000000, 9999999)
    current_employees = Employee.get_all()
    booleanval = True
    for current_employee in current_employees:
        if current_employee.employee_id == new_employee_number:
            booleanval = False
        else:
            pass
    if booleanval == True:
        return new_employee_number
    else:
        return en_generator()

# Generates and validates new standardized ticket numbers
def tn_generator():
    new_ticket_number = "Z" + str(random.randrange(100000000, 999999999))
    current_tickets = Ticket.get_all()
    booleanval = True
    for current_ticket in current_tickets:
        if current_ticket.ticket_number == new_ticket_number:
            booleanval = False
        else:
            pass
    if booleanval == True:
        return new_ticket_number
    else:
        return tn_generator()

def new_ticket(employee):
    sweep_up_shop()
    employee_number = employee.id
    timestamp = str(datetime.datetime.now())
    issues = Issue.get_all()
    print("Enter a number not being used to create a new issue.")
    for issue in issues:
        print(f"Code: {issue.issue_code} ; {issue.issue_desc}")
    selection = input("Please select an issue code: ")
    if selection := Issue.find_by_issue_code(selection):
        try:
            new_ticket = Ticket.create(tn_generator(), employee_number, selection.id, timestamp)
            sweep_up_shop()
            new_object = f"""Please retain this information.\n
Employee: {employee.name}\n
Ticket Number: {new_ticket.ticket_number}\n
Issue Code: {selection.issue_code}\n
{selection.issue_desc}\n
Processing time is approx. {selection.process_time} days."""
            success_screen(new_object)
        except Exception as exc:
            error_screen(exc)
    else:
        sweep_up_shop()
        print("Issue Code Not Found.")
        print("Would you like to create a new issue?")
        print("Y / N")
        choice = input("> ")
        if choice == "y":
            pass
        elif choice == "n":
            pass
        else:
            error_screen("Invalid option.")

def user_view_tickets(employee):
    sweep_up_shop()
    print(f"Showing All Open Tickets for {employee.name}")
    print("")
    tickets = Ticket.get_all()
    for ticket in tickets:
        if ticket.employee == employee.id:
            issue = Issue.find_by_id(ticket.issue)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Ticket Number: {ticket.ticket_number}")
            print(f"Code: {issue.issue_code}")
            print(f"{issue.issue_desc}")
            print(f"Posted @ {ticket.timestamp}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            pass
    print("End of List")
    print("")
    print("Press enter to continue, or type the ticket number for more options.")
    print("")
    selection = input(">>> ")
    ticket = Ticket.find_by_ticket_number(selection)
    if selection == "":
        pass
    elif ticket == None:
        error_screen("Ticket not found.")
    else:
        user_edit_ticket(ticket)

def user_edit_ticket(ticket):
    sweep_up_shop()
    issue = Issue.find_by_id(ticket.issue)
    employee = Employee.find_by_id(ticket.employee)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Ticket Number: {ticket.ticket_number}")
    print(f"Posted by: {employee.name}")
    print(f"Issue Code: {issue.issue_code}")
    print(f"{issue.issue_desc}")
    print(f"Posted @ {ticket.timestamp}")
    print(f"Processing Time is approx. {issue.process_time} days")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("Would you like to mark this ticket as resolved?")
    print("Enter Y / N")
    print("")
    choice = input("> ")
    if choice == "y":
        try:
            old_ticket = ticket.ticket_number
            ticket.delete()
            success_screen(f"Marked Ticket {old_ticket} as Resolved!")
        except Exception as exc:
            error_screen(exc)
    elif choice == "n":
        pass
    else:
        error_screen("Invalid selection.")

def admin_view_all_tickets():
    sweep_up_shop()
    print("Showing All Open Tickets")
    print("")
    tickets = Ticket.get_all()
    for ticket in tickets:
        issue = Issue.find_by_id(ticket.issue)
        employee = Employee.find_by_id(ticket.employee)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Ticket Number: {ticket.ticket_number}")
        print(f"Employee: {employee.name}")
        print(f"Employee Contact: {employee.contact_information}")
        print(f"Code: {issue.issue_code}")
        print(f"{issue.issue_desc}")
        print(f"Posted @ {ticket.timestamp}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("End of List")
    print("")
    print("Press enter to continue, or type the ticket number for more options.")
    print("")
    selection = input(">")
    ticket = Ticket.find_by_ticket_number(selection)
    if selection == "":
        pass
    elif ticket == None:
        error_screen("Ticket not found.")
    else:
        admin_edit_ticket(ticket)

def admin_edit_ticket(ticket):
    sweep_up_shop()
    issue = Issue.find_by_id(ticket.issue)
    employee = Employee.find_by_id(ticket.employee)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Ticket Number: {ticket.ticket_number}")
    print(f"Employee: {employee.name}")
    print(f"Employee Contact: {employee.contact_information}")
    print(f"Issue Code: {issue.issue_code}")
    print(f"{issue.issue_desc}")
    print(f"Posted @ {ticket.timestamp}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("Would you like to mark this ticket as resolved?")
    print("Enter Y / N")
    print("")
    choice = input("> ")
    if choice == "y":
        try:
            old_ticket = ticket.ticket_number
            ticket.delete()
            success_screen(f"Marked Ticket {old_ticket} as Resolved!")
        except Exception as exc:
            error_screen(exc)
    elif choice == "n":
        pass
    else:
        error_screen("Invalid selection.")

def create_employee():
    sweep_up_shop()
    name = input("Please enter name: ")
    employee_id = en_generator()
    contact = input("Please enter employee email: ")
    print("Please add employee permissions. Enter a for admin and u for user.")
    permissions = input("> ")
    if permissions == 'a':
        access_level = "admin"
    elif permissions == 'u':
        access_level = "user"
    else:
        error_screen("Invalid input.")
    try:
        new_employee = Employee.create(name, employee_id, contact, access_level)
        success_screen(f"{new_employee.name} has been added!")
    except Exception as exc:
        error_screen(exc)

def edit_employee():
    sweep_up_shop()
    employee_to_edit = input("Please enter the employee ID to edit: ")
    employee_instance = Employee.find_by_employee_id(employee_to_edit)
    if employee_instance == None:
        error_screen("Employee ID not found.")
    else:
        try:
            sweep_up_shop()
            print(f"Editing Employee {employee_instance.name}")
            employee_instance.name = input("Please enter employee's new name: ")
            employee_instance.contact_information = input("Please enter employee's new email: ")
            print(f"What permissions would you like {employee_instance.name} to have?")
            print("(a for 'Admin' and u for 'User')")
            permissions = input("> ")
            if permissions == 'a':
                employee_instance.access_level = "admin"
            elif permissions == 'u':
                employee_instance.access_level = "user"
            else:
                error_screen("Invalid Input")
            employee_instance.update()
            success_screen(f"{employee_instance.name} has been updated!")
        except Exception as exc:
            error_screen(exc)

def delete_employee():
    sweep_up_shop()
    employee_to_delete = input("Please enter the employee ID to remove: ")
    employee_instance = Employee.find_by_employee_id(employee_to_delete)
    if employee_instance == None:
        error_screen("Employee ID not found.")
    else:
        employee_instance.delete()
        success_screen(f"{employee_instance.name} has been removed!")

def edit_tickets_by_employee_id():
    sweep_up_shop()
    print("Please enter the 7 digit employee ID:")
    employee_id = input("> ")
    employee = Employee.find_by_employee_id(employee_id)
    ticket_instances = Ticket.find_by_employee(employee.id)
    if employee == None:
        error_screen("Employee not found.")
    else:
        sweep_up_shop()
        print(f"Showing All Tickets for {employee.name}")
        for ticket in ticket_instances:
            issue = Issue.find_by_id(ticket.issue)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Ticket Number: {ticket.ticket_number}")
            print(f"Employee: {employee.name}")
            print(f"Employee Contact: {employee.contact_information}")
            print(f"Code: {issue.issue_code}")
            print(f"{issue.issue_desc}")
            print(f"Posted @ {ticket.timestamp}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("End of List")
        print("")
        print("Press enter to continue, or type the ticket number for more options.")
        print("")
        selection = input(">")
        ticket = Ticket.find_by_ticket_number(selection)
        if selection == "":
            pass
        elif ticket == None:
            error_screen("Ticket not found.")
        else:
            admin_edit_ticket(ticket)

def edit_tickets_by_ticket_no():
    sweep_up_shop()
    print("Please enter the ticket number:")
    ticket = input("> ")
    ticket_instance = Ticket.find_by_ticket_number(ticket)
    if ticket_instance == None:
        error_screen("Ticket not found.")
    else:
        admin_edit_ticket(ticket_instance)