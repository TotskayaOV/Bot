from external_database import *
import datetime
from working_database import DataBase
from send_massage import notify
from loader import db

def chat_text(data: dict):
    text_mess = f"ФИО:{data.get('agent_name')}\nТелефон: {data.get('phone_number')}\n" \
                f"ИНН:{data.get('inn_number')}\nКомпания: {data.get('company_name')}"
    return text_mess


def cheking_list(num_com: int, number_list: list, values: dict):
    for i in range(len(number_list)):
        data = writing_data(num_com, number_list[i], values)
        res = db.get_dump_agent(agent_name=data.get('agent_name'))
        if not res:
            if (data.get('inn_number') == '') or (data.get('phone_number') == ''):
                my_adminset = db.get_user_access(user_role='admin')
                for y in range(len(my_adminset)):
                    chat_id = my_adminset[y][1]
                    text_mess = chat_text(data) + "\nНЕДОСТАТОЧНО ДАННЫХ"
                    notify(chat_id, text_mess)
                    dump_data = {'agent_name': data.get('agent_name'), 'phone_number': data.get('phone_number'),
                                'inn_number': data.get('inn_number'), 'company_name': data.get('company_name'),
                                'date_up': datetime.datetime.now(), 'row_number': number_list[i], 'comment': ''}
                    db.add_dump_agent(dump_data)
                my_divset = db.get_user_access(user_role='divisional_mentor')
                for y in range(len(my_divset)):
                    chat_id = my_divset[y][1]
                    text_mess = chat_text(data) + "\nНЕДОСТАТОЧНО ДАННЫХ"
                    notify(chat_id, text_mess)
            else:
                my_adminset = db.get_user_access(user_role='admin')
                for y in range(len(my_adminset)):
                    chat_id = my_adminset[y][1]
                    text_mess = chat_text(data)
                    notify(chat_id, text_mess)
                    dump_data = {'agent_name': data.get('agent_name'), 'phone_number': data.get('phone_number'),
                                'inn_number': data.get('inn_number'), 'company_name': data.get('company_name'),
                                'date_up': datetime.datetime.now(), 'row_number': number_list[i], 'comment': ''}
                    db.add_dump_agent(dump_data)
                my_coorset = db.get_user_access(user_role='coordinator')
                for y in range(len(my_coorset)):
                    chat_id = my_coorset[y][1]
                    text_mess = chat_text(data)
                    notify(chat_id, text_mess)


def cheking_workbase():
    values_IM = google_search().get('ИЗИМСК')
    values_Yg = google_search().get('ЯГО')
    values_Lk = google_search().get('ЛКАРГО')
    numbers_IM = column_comparison(values_IM)
    numbers_Yg = column_comparison(values_Yg)
    numbers_Lk = column_comparison(values_Lk)
    if len(numbers_IM) != 0:
        cheking_list(1, numbers_IM, values_IM)
    if len(numbers_Yg) != 0:
        cheking_list(2, numbers_Yg, values_Yg)
    if len(numbers_Lk) != 0:
        cheking_list(3, numbers_Lk, values_Lk)

