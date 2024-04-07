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

    @property
    def issue_code(self):
        return self._issue_code
    
    ### Needs to verify that the issue code doesn't already exist ###

    @issue_code.setter
    def issue_code(self, issue_code):
        if isinstance(issue_code, int) and len(issue_code) is 3:
            self._issue_code = issue_code
        else:
            raise ValueError("Issue Code must be a 3 digit integer")
        
    @property
    def sub_cat(self):
        return self._sub_cat
    
    @sub_cat.setter
    def sub_cat(self, sub_cat):
        if isinstance(sub_cat, str) and sub_cat is "hardware" or "software" or "permissions" or "other":
            self._sub_cat = sub_cat
        else:
            raise ValueError("Sub-Category must be 'hardware', 'software', 'permissions', or 'other'.")
    
    @property
    def issue_desc(self):
        return self._issue_desc
    
    @issue_desc.setter
    def issue_desc(self, issue_desc):
        if isinstance(issue_desc, str) and len(issue_desc) > 0:
            self._issue_desc = issue_desc
        else:
            raise ValueError("Issue must be a non-empty string")
        
    @property
    def process_time(self):
        return self._process_time
    
    @process_time.setter
    def process_time(self, process_time):
        if isinstance(process_time, int):
            self._process_time = process_time
        else:
            raise ValueError("Processing time must be an integer representing days.")
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            issue_code INTEGER,
            sub_cat TEXT,
            issue_desc TEXT,
            process_time INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS tickets
        """
        CURSOR.execute(sql)
        CONN.execute()

    def save(self):
        sql = """
            INSERT INTO tickets (issue_code, sub_cat, issue_desc, process_time)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.issue_code, self.sub_cat, self.issue_desc, self.process_time))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, issue_code, sub_cat, issue_desc, process_time):
        ticket = cls(issue_code, sub_cat, issue_desc, process_time)
        ticket.save()
        return ticket
    
    def update(self):
        sql = """
            UPDATE tickets
            SET issue_code = ?, sub_cat = ?, issue_desc = ?, process_time = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.issue_code, self.sub_cat, self.issue_desc, self.process_time, self.id))
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
    def instance_from_db(cls, row):
        ticket = cls.all.get(row[0])
        if ticket:
            ticket.issue_code = row[1]
            ticket.sub_cat = row[2]
            ticket.issue_desc = row[3]
            ticket.process_time = row[4]
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
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_issue_code(cls, issue_code):
        sql = """
            SELECT *
            FROM tickets
            WHERE issue_code = ?
        """
        row = CURSOR.execute(sql, (issue_code,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_sub_category(cls, sub_cat):
        sql = """
            SELECT *
            FROM tickets
            WHERE sub_cat = ?
        """
        rows = CURSOR.execute(sql, (sub_cat,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]