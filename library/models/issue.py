from models.__init__ import CURSOR, CONN

class Issue:

    all = {}

    def __init__(self, issue_code, sub_cat, issue_desc, process_time, id=None):
        self.id = id
        self.issue_code = issue_code
        self.sub_cat = sub_cat
        self.issue_desc = issue_desc
        self.process_time = process_time

    def __repr__(self):
        return f'<Issue {self.id}: {self.issue_code}, {self.sub_cat}, {self.issue_desc}, {self.process_time}>'
