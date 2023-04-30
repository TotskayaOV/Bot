import sqlite3


class DataBase:
    def __init__(self, db_path: str = './cred/bot_db.db'):
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
        company_name TEXT, date_up DATETIME, date_down DATETIME, comment TEXT, last_user INTEGER)'''
        self.execute(sql, commit=True)


    def create_table_user_access(self):
        sql = '''CREATE TABLE IF NOT EXISTS user_access 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, name TEXT, user_role TEXT)'''
        self.execute(sql, commit=True)


    def create_table_dump_agent(self):
        sql = '''CREATE TABLE IF NOT EXISTS dump_agent 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, phone_number INTEGER, inn_number INTEGER, 
        company_name TEXT, date_up DATETIME, row_number INTEGER, comment TEXT)'''
        self.execute(sql, commit=True)


    def create_table_dump_comment(self):
        sql = '''CREATE TABLE IF NOT EXISTS dump_comment 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, company_name TEXT, 
        phone_number INTEGER, inn_number INTEGER, 
        comment TEXT, date_up DATETIME, user_id INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_task_kick(self):
        sql = '''CREATE TABLE IF NOT EXISTS task_kick 
        (id_task INTEGER PRIMARY KEY,
        message_time DATETIME, count_kick INTEGER)'''
        self.execute(sql, commit=True)


    def create_list_mentors(self):
        sql = '''CREATE TABLE IF NOT EXISTS mentors 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, name TEXT, user_tag TEXT, city TEXT)'''
        self.execute(sql, commit=True)


    def add_com_applications(self, com_applications: dict):
        parameters = (com_applications.get('agent_name'), com_applications.get('phone_number'),
                      com_applications.get('inn_number'), com_applications.get('company_name'),
                      com_applications.get('date_up'), com_applications.get('date_down'),
                      com_applications.get('comment'), com_applications.get('last_user'))
        sql = '''INSERT INTO com_applications (agent_name, phone_number, inn_number, company_name, 
        date_up, date_down, comment, last_user) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def add_user_access(self, user_access: dict):
        parameters = (user_access.get('user_id'), user_access.get('name'), user_access.get('user_role'))
        sql = '''INSERT INTO user_access (user_id, name, user_role) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def add_list_mentors(self, user_access: dict):
        parameters = (user_access.get('user_id'), user_access.get('name'),
                      user_access.get('user_tag'), user_access.get('city'))
        sql = '''INSERT INTO mentors (user_id, name, user_tag, city) 
        VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def add_dump_agent(self, dump_agent: dict):
        parameters = (dump_agent.get('agent_name'), dump_agent.get('phone_number'), dump_agent.get('inn_number'),
                      dump_agent.get('company_name'), dump_agent.get('date_up'), dump_agent.get('row_number'),
                      dump_agent.get('comment'))
        sql = '''INSERT INTO dump_agent (agent_name, phone_number, inn_number, company_name, date_up, row_number, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def add_task_kick(self, task_data: dict):
        parameters = (task_data.get('id_task'), task_data.get('message_time'), task_data.get('count_kick'))
        sql = '''INSERT INTO task_kick (id_task, message_time, count_kick)
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)


    def add_comment_to_repository(self, dump_agent: dict):
        parameters = (dump_agent.get('agent_name'), dump_agent.get('company_name'),
                      dump_agent.get('phone_number'), dump_agent.get('inn_number'),
                      dump_agent.get('comment'), dump_agent.get('date_up'), dump_agent.get('user_id'))
        sql = '''INSERT INTO dump_comment (agent_name, company_name, phone_number, inn_number, 
        comment, date_up, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def update_dump_comm(self, dump_agent: dict):
        parameters = (dump_agent.get('agent_name'), dump_agent.get('phone_number'), dump_agent.get('inn_number'),
                      dump_agent.get('comment'), dump_agent.get('id'))
        sql = '''UPDATE dump_agent SET agent_name=?, phone_number=?, inn_number=?, comment=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)


    def update_task_kick(self, task_data: dict):
        parameters = (task_data.get('count_kick'), task_data.get('id_task'))
        sql = '''UPDATE task_kick SET count_kick=? WHERE id_task=? '''
        self.execute(sql, parameters, commit=True)


    def add_dump_comm(self, dump_agent: dict):
        parameters = (dump_agent.get('comment'), dump_agent.get('inn_number'))
        sql = '''UPDATE dump_agent SET comment=? WHERE inn_number=?'''
        self.execute(sql, parameters, commit=True)


    def add_dump_comm_phone(self, dump_agent: dict):
        parameters = (dump_agent.get('comment'), dump_agent.get('phone_number'))
        sql = '''UPDATE dump_agent SET comment=? WHERE phone_number=?'''
        self.execute(sql, parameters, commit=True)


    def get_all_com_applications(self):
        sql = '''SELECT * FROM com_applications'''
        return self.execute(sql, fetchall=True)


    def get_all_user_access(self):
        sql = '''SELECT * FROM user_access'''
        return self.execute(sql, fetchall=True)

    def get_all_comment_to_repository(self):
        sql = '''SELECT * FROM dump_comment'''
        return self.execute(sql, fetchall=True)


    def get_all_mentors(self):
        sql = '''SELECT * FROM mentors'''
        return self.execute(sql, fetchall=True)


    def get_all_dump_agent(self):
        sql = '''SELECT * FROM dump_agent'''
        return self.execute(sql, fetchall=True)


    def get_all_task_kick(self):
        sql = '''SELECT * FROM task_kick'''
        return self.execute(sql, fetchall=True)


    def get_com_applications(self, **kwargs):
        sql = '''SELECT * FROM com_applications WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def get_done_com_applications(self, date1):
        parameters = (date1, )
        sql = '''SELECT * FROM com_applications WHERE date_up>?'''
        return self.execute(sql, parameters, fetchall=True)


    def get_user_access(self, **kwargs):
        sql = '''SELECT * FROM user_access WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def get_list_mentors(self, **kwargs):
        sql = '''SELECT * FROM mentors WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def get_dump_agent(self, **kwargs):
        sql = '''SELECT * FROM dump_agent WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def get_comment_to_repository(self, **kwargs):
        sql = '''SELECT * FROM dump_comment WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)


    def remove_user(self, id_user: int):
        parameters = (id_user,)
        sql = '''DELETE FROM user_access WHERE user_id=?'''
        self.execute(sql, parameters, commit=True)


    def remove_mentors(self, id_user: int):
        parameters = (id_user,)
        sql = '''DELETE FROM mentors WHERE user_id=?'''
        self.execute(sql, parameters, commit=True)


    def remove_table_com_applications(self, id: int):
        parameters = (id,)
        sql = '''DELETE FROM com_applications WHERE id=?'''
        self.execute(sql, parameters, commit=True)


    def remove_dump_agent(self, id: int):
        parameters = (id,)
        sql = '''DELETE FROM dump_agent WHERE id=?'''
        self.execute(sql, parameters, commit=True)

    def remove_task_kick(self, id_task: int):
        parameters = (id_task,)
        sql = '''DELETE FROM task_kick WHERE id_task=?'''
        self.execute(sql, parameters, commit=True)


    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())


    def disconnect(self):
        self.connection.close()
