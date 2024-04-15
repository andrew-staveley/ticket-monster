from models.__init__ import CONN, CURSOR
from models.employee import Employee
from models.issue import Issue
from models.ticket import Ticket
from helpers import tn_generator, en_generator
from faker import Faker
import datetime

fake = Faker()

def seed_database():
    Employee.drop_table()
    Issue.drop_table()
    Ticket.drop_table()
    Employee.create_table()
    Issue.create_table()
    Ticket.create_table()

    employee_one = Employee.create("ADMIN TEST", 1111111, "admin@company.com", "admin")
    employee_two = Employee.create("USER TEST", 2222222, "user@company.com", "user")
    employee_three = Employee.create(fake.name(), en_generator(), fake.email(), "user")
    employee_four = Employee.create(fake.name(), en_generator(), fake.email(), "user")
    employee_five = Employee.create(fake.name(), en_generator(), fake.email(), "user")
    Employee.create(fake.name(), en_generator(), fake.email(), "user")
    Employee.create(fake.name(), en_generator(), fake.email(), "user")
    Employee.create(fake.name(), en_generator(), fake.email(), "user")



    issue_one = Issue.create(101, "hardware", "Computer won't connect to internet.", 1)
    issue_two = Issue.create(102, "hardware", "Computer won't turn on.", 3)
    issue_three = Issue.create(103, "hardware", "Computer won't charge.", 1)
    issue_four = Issue.create(201, "software", "Program license expired.", 2)
    issue_five = Issue.create(202, "software", "Computer needs an OS update.", 2)
    issue_six = Issue.create(203, "software", "Download new software suite.", 3)
    issue_seven = Issue.create(301, "permissions", "Password needs to be reset.", 1)
    issue_eight = Issue.create(302, "permissions", "Change from 'user' to 'admin'.", 1)
    issue_nine = Issue.create(303, "permissions", "No access to software.", 1)
    issue_ten = Issue.create(401, "other", "Computer fell into lake while working from 'home'", 5)

    Ticket.create(tn_generator(), employee_one.id, issue_one.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_two.id, issue_two.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_three.id, issue_three.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_four.id, issue_four.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_one.id, issue_five.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_two.id, issue_six.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_three.id, issue_seven.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_four.id, issue_eight.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_one.id, issue_nine.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_two.id, issue_ten.id, str(datetime.datetime.now()))
    Ticket.create(tn_generator(), employee_five.id, issue_eight.id, str(datetime.datetime.now()))


seed_database()
print("Seeded Database")
