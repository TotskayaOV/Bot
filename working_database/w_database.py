import sqlite3

class DataBase:
    def __init__(self, db_path: str = 'data_base/bot_db.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_com_applications(self):
        sql = '''CREATE TABLE IF NOT EXISTS com_applications 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, phone_number INTEGER, inn_number INTEGER, 
        company_name TEXT)'''
        self.execute(sql, commit=True)

    def create_table_user_access(self):
        sql = '''CREATE TABLE IF NOT EXISTS user_access 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, name TEXT, user_role TEXT)'''
        self.execute(sql, commit=True)

    def add_com_applications(self, com_applications: dict):
        parameters = (com_applications.get('agent_name'), com_applications.get('phone_number'), com_applications.get('inn_number'),
                      com_applications.get('company_name'))
        sql = '''INSERT INTO com_applications (agent_name, phone_number, inn_number, company_name) 
        VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_user_access(self, user_access: dict):
        parameters = (user_access.get('user_id'), user_access.get('name'), user_access.get('user_role'))
        sql = '''INSERT INTO user_access (user_id, name, user_role) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def get_com_applications(self, **kwargs):
        sql = '''SELECT * FROM com_applications WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_user_access(self, **kwargs):
        sql = '''SELECT * FROM user_access WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def remove_user(self, id_user: int):
        parameters = (id_user,)
        sql = '''DELETE FROM user_access WHERE user_id=?'''
        self.execute(sql, parameters, commit=True)


    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()