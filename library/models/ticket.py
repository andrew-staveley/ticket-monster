from models.__init__ import CURSOR, CONN
from models.employee import Employee
from models.issue import Issue

class Ticket:

    all = {}

    def __init__(self, ticket_number, employee, issue, timestamp, id=None):
        self.id = id
        self.ticket_number = ticket_number
        self.employee = employee
        self.issue = issue
        self.timestamp = timestamp

    def __repr__(self):
        return f'<Ticket No.: {self.ticket_number} Posted By: {self.employee_id} Issue Code: {self.issue_code} ; {self.extra} @ {self.timestamp}>'
    
    @property
    def ticket_number(self):
        return self._ticket_number
    
    @ticket_number.setter
    def ticket_number(self, ticket_number):
        if isinstance(ticket_number, str) and len(ticket_number) == 10 and ticket_number[0] == "Z":
            self._ticket_number = ticket_number
        else:
            raise ValueError("Ticket number must be a 10 character string with the first character being Z.")
        
    @property
    def employee(self):
        return self._employee
    
    @employee.setter
    def employee(self, employee):
        if type(employee) is int and Employee.find_by_id(employee):
            self._employee = employee
        else:
            raise ValueError("Employee must reference to an employee in the database. NOTE: This is asking for the DATABASE ID (Column One), not the actual EMPLOYEE ID.")
        
    @property
    def issue(self):
        return self._issue

    @issue.setter
    def issue(self, issue):
        if type(issue) is int and Issue.find_by_id(issue):
            self._issue = issue
        else:
            raise ValueError("Issue Code must reference to an issue in the database. NOTE: This is asking for the DATABASE ID (Column One), not the actual ISSUE CODE.")
        
    @property
    def timestamp(self):
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp):
        if isinstance(timestamp, str):
            self._timestamp = timestamp
        else:
            raise ValueError("Timestamp must be a string.")
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            ticket_number STR,
            employee INT,
            issue INT,
            timestamp STR,
            FOREIGN KEY (employee) REFERENCES employees(id),
            FOREIGN KEY (issue) REFERENCES issues(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS tickets
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO tickets (ticket_number, employee, issue, timestamp)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.ticket_number, self.employee, self.issue, self.timestamp))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        sql = """
            UPDATE tickets
            SET ticket_number = ?, employee = ?, issue = ?, timestamp = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.ticket_number, self.employee, self.issue, self.timestamp, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM tickets
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, ticket_number, employee, issue, timestamp):
        ticket = cls(ticket_number, employee, issue, timestamp)
        ticket.save()
        return ticket
    
    @classmethod
    def instance_from_db(cls, row):
        ticket = cls.all.get(row[0])
        if ticket:
            ticket.ticket_number = row[1]
            ticket.employee = row[2]
            ticket.issue = row[3]
            ticket.timestamp = row[4]
        else:
            ticket = cls(row[1], row[2], row[3], row[4])
            ticket.id = row[0]
            cls.all[ticket.id] = ticket
        return ticket
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM tickets
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM tickets
            WHERE id is ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_employee(cls, employee):
        sql = """
            SELECT *
            FROM tickets
            WHERE employee is ?
        """
        rows = CURSOR.execute(sql, (employee,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_ticket_number(cls, ticket):
        sql = """
            SELECT *
            FROM tickets
            WHERE ticket_number is ?
        """
        row = CURSOR.execute(sql, (ticket,)).fetchone()
        return cls.instance_from_db(row) if row else None