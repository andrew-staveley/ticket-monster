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
    print("Success! You're request was completed!")
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
    employee_number = employee[0]
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
Employee: {employee[1]}\n
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
    print(f"Showing All Open Tickets for {employee[1]}")
    print("")
    tickets = Ticket.get_all()
    for ticket in tickets:
        if ticket.employee == employee[0]:
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