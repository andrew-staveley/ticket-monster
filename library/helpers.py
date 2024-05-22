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
        if current_employee.employee_number == new_employee_number:
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

def new_ticket(employee, subcat):
    sweep_up_shop()
    issues = Issue.find_by_sub_category(subcat)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Press enter to make a new issue code.")
    for issue in issues:
        print(f"Code: {issue.issue_code} ; {issue.issue_desc}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    selection = input("Please enter an issue code: ")
    if selection := Issue.find_by_issue_code(selection):
        try:
            new_ticket = Ticket.create(tn_generator(), employee.id, selection.id, str(datetime.datetime.now()))
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
            new_issue(employee, subcat)
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
        print(f"Issue Code: {issue.issue_code}")
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
    employee_number = en_generator()
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
        new_employee = Employee.create(name, employee_number, contact, access_level)
        success_screen(f"{new_employee.name} has been added!")
    except Exception as exc:
        error_screen(exc)

def edit_employee():
    sweep_up_shop()
    employee_list()
    print("")
    employee_to_edit = input("Please enter the employee number to edit: ")
    employee_instance = Employee.find_by_employee_number(employee_to_edit)
    if employee_instance == None:
        error_screen("Employee number not found.")
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
    employee_list()
    print("")
    employee_to_delete = input("Please enter the employee number to remove: ")
    employee_instance = Employee.find_by_employee_number(employee_to_delete)
    if employee_instance == None:
        error_screen("Employee number not found.")
    else:
        employee_tickets = employee_instance.tickets()
        for ticket in employee_tickets:
            ticket.delete()
        employee_instance.delete()
        success_screen(f"{employee_instance.name} & associated tickets have been removed!")

def edit_tickets_by_employee_id():
    sweep_up_shop()
    print("Please enter the 7 digit employee number:")
    employee = Employee.find_by_employee_number(input("> "))
    if employee == None:
        error_screen("Employee not found.")
    else:
        sweep_up_shop()
        print(f"Showing All Tickets for {employee.name}")
        for ticket in employee.tickets():
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

def new_issue(employee, subcat):
    sweep_up_shop()
    issue_instances = Issue.find_by_sub_category(subcat)
    new_issue_code = issue_instances[-1].issue_code + 1
    if Issue.find_by_issue_code(new_issue_code) == None:
        print("Please enter a description of the issue.")
        issue_desc = input("> ")
        if employee.access_level == "admin":
            print("Please enter a number to represent the amount of days until completion.")
            time = input("> ")
        else:
            time = 0
        try:
            Issue.create(new_issue_code, subcat, issue_desc, int(time))
            success_screen(f"Issue {new_issue_code} has been created!\nPlease be aware that if a ticket was trying to be created, it will have to be resubmitted with the new issue code.")
        except Exception as exc:
            error_screen(exc)
    else:
        error_screen("Internal Error, Please try again later.")

def edit_issue():
    sweep_up_shop()
    issues = Issue.get_all()
    for issue in issues:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Issue Code: {issue.issue_code}")
        print(f"Sub-Category: {issue.sub_cat}")
        print(f"{issue.issue_desc}")
        print(f"Processing time is {issue.process_time} days.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("End of List")
    print("")
    print("Enter an item code to edit, or press enter to exit.")
    choice = input("> ")
    if choice == "":
        pass
    else:
        fetched_issue = Issue.find_by_issue_code(choice)
        if fetched_issue:
            sweep_up_shop()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Issue Code: {fetched_issue.issue_code}")
            print(f"Sub-Category: {fetched_issue.sub_cat}")
            print(f"{fetched_issue.issue_desc}")
            print(f"Processing time is {fetched_issue.process_time} days.")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            try:
                fetched_issue.issue_code = fetched_issue.issue_code
                fetched_issue.sub_cat = fetched_issue.sub_cat
                desc = input("Please enter a new description (leave blank to skip): ")
                if desc == "":
                    fetched_issue.issue_desc = fetched_issue.issue_desc
                else:
                    fetched_issue.issue_desc = desc
                time = input("Please enter a processing time in days: ")
                fetched_issue.process_time = int(time)
                fetched_issue.update()
                success_screen(f"Issue {fetched_issue.issue_code} has been updated!")
            except Exception as exc:
                error_screen(exc)
        else:
            error_screen("Issue Code not Found")

def remove_issue():
    sweep_up_shop()
    issues = Issue.get_all()
    for issue in issues:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Issue Code: {issue.issue_code}")
        print(f"Sub-Category: {issue.sub_cat}")
        print(f"{issue.issue_desc}")
        print(f"Processing time is {issue.process_time} days.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("End of List")
    print("")
    print("Enter an issue code to delete, or press enter to exit.")
    choice = input("> ")
    if choice == "":
        pass
    elif issue_to_delete := Issue.find_by_issue_code(choice):
        try:
            issue_to_delete.delete()
            success_screen(f"Issue {choice} has been deleted!")
        except Exception as exc:
            error_screen(exc)
    else:
        error_screen("Issue code not found.")

def view_issues():
    sweep_up_shop()
    issues = Issue.get_all()
    for issue in issues:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Issue Code: {issue.issue_code}")
        print(f"Sub-Category: {issue.sub_cat}")
        print(f"{issue.issue_desc}")
        print(f"Processing time is {issue.process_time} days.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("End of List")
    print("")
    print("Press Enter to Continue")
    input("> ")

def employee_list():
    sweep_up_shop()
    employees = Employee.get_all()
    print(("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))
    for employee in employees:
        print(f"{employee.name} <{employee.employee_number}>")
    print(("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))