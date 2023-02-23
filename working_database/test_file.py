from working_database import DataBase
db = DataBase(db_path=db_path)
# kwarg_dict = {}
# kwarg_dict = 'admin'
print(DataBase.db.get_user_access(user_role='admin'))