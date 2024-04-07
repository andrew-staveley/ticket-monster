from models.__init__ import CURSOR, CONN

class Ticket:

    all = {}

    def __init__(self, ticket_number, employee_id, issue_code, extra, timestamp, id=None):
        self.id = id
        self.ticket_number = ticket_number
        self.employee_id = employee_id
        self.issue_code = issue_code
        self.extra = extra
        self.timestamp = timestamp

    def __repr__(self):
        return f'<Ticket No.: {self.ticket_number} Posted By: {self.employee_id} Issue Code: {self.issue_code} ; {self.extra} @ {self.timestamp}>'