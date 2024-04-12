from models.__init__ import CURSOR, CONN

class Employee:

    all = {}

    def __init__(self, name, employee_id, contact_information, access_level, id=None):
        self.id = id
        self.name = name
        self.employee_id = employee_id
        self.contact_information = contact_information
        self.access_level = access_level

    def __repr__(self):
        return f'<Employee {self.id}: {self.name} {self.contact_information}, Employee ID: {self.employee_id} Access Level: {self.access_level}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string.")
        
    @property
    def employee_id(self):
        return self._employee_id

    ### This also needs to verify that the employee ID that was entered isn't already in use. ###

    @employee_id.setter
    def employee_id(self, employee_id):
        if isinstance(employee_id, int) and len(str(employee_id)) == 7:
            self._employee_id = employee_id
        else:
            raise ValueError("Employee ID must be a 7 digit integer.")
        
    @property
    def contact_information(self):
        return self._contact_information
    
    ### This could use some sort of validation to determine if the entered value is a valid email, and also not in use ###

    @contact_information.setter
    def contact_information(self, contact_information):
        if isinstance(contact_information, str):
            self._contact_information = contact_information
        else:
            raise ValueError("Contact information must be an email.")
        
    @property
    def access_level(self):
        return self._access_level
    
    @access_level.setter
    def access_level(self, access_level):
        if access_level == "admin" or "user":
            self._access_level = access_level
        else:
            raise ValueError("Access level must be either 'user' or 'admin'.")
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            employee_id INT,
            contact_information TEXT,
            access_level TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """ DROP TABLE IF EXISTS employees """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO employees (name, employee_id, contact_information, access_level)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.employee_id, self.contact_information, self.access_level))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, employee_id, contact_information, access_level):
        employee = cls(name, employee_id, contact_information, access_level)
        employee.save()
        return employee
    
    def update(self):
        sql = """
            UPDATE employees
            SET name = ?, employee_id = ?, contact_information = ?, access_level = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.employee_id, self.contact_information, self.access_level, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM employees
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
    
    @classmethod
    def instance_from_db(cls, row):
        employee = cls.all.get(row[0])
        if employee:
            employee.name = row[1]
            employee.employee_id = row[2]
            employee.contact_information = row[3]
            employee.access_level = row[4]
        else:
            employee = cls(row[1], row[2], row[3], row[4])
            employee.id = row[0]
            cls.all[employee.id] = employee
        return employee
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM employees
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM employees
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM employees
            WHERE name is ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_employee_id(cls, employee_id):
        sql = """
            SELECT *
            FROM employees
            WHERE employee_id is ?
        """
        obj = CURSOR.execute(sql, (employee_id,)).fetchone()
        #return cls.instance_from_db(row) if row else None
        return obj
    
    def tickets(self):
        from models.ticket import Ticket
        sql = """
            SELECT * FROM ticketsx
            WHERE employee = ?
        """
        CURSOR.execute(sql, (self.id,),)
        rows = CURSOR.fetchall()
        return [
            Ticket.instance_from_db(row) for row in rows
        ]