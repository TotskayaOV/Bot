from external_database import *
import datetime
from working_database import DataBase
from send_massage import notify
from loader import db, dp
from keyboards import kb_coord_inline


# Формирует строку для отправки сообщения
def chat_text(data: dict):
    text_mess = f"ФИО:{data.get('agent_name')}\nТелефон: {data.get('phone_number')}\n" \
                f"ИНН:{data.get('inn_number')}\nКомпания: {data.get('company_name')}"
    return text_mess


# Формирует словарь для записи в ДБ (таблица агенты в работе - dump_agent)
def send_to_dump(row_number: int, data: dict):
    dump_data = {'agent_name': data.get('agent_name'), 'phone_number': data.get('phone_number'),
                 'inn_number': data.get('inn_number'), 'company_name': data.get('company_name'),
                 'date_up': datetime.datetime.now(), 'row_number': row_number, 'comment': ''}
    return dump_data


# Проходит по индексам полученного списка. Передает данные в функцию, которая формирует карточку агента в виде словаря
# Проверяет наличие этого агента по ФИО среди тех кто уже находится в работе. Если его там нет, проверяет карточку
# на полноту данных. Если данные не полные, то отправляет сообщене ДН и админам (списки с id_user my_divset и my_adminset через
# notify). В конце передает карточку для записи в dump (данные формируются через send_to_dump).
async def cheking_list(num_com: int, number_list: list, values: dict):
    for i in range(len(number_list)):
        data = writing_data(num_com, number_list[i], values)
        check_dump = db.get_dump_agent(agent_name=data.get('agent_name'))
        my_adminset = db.get_user_access(user_role='admin')
        if not check_dump:
            if (data.get('inn_number') == '') or (data.get('phone_number') == ''):
                my_divset = db.get_user_access(user_role='divisional_mentor')
                if my_divset:
                    my_adminset.extend(my_divset)
                for y in range(len(my_adminset)):
                    chat_id = my_adminset[y][1]
                    text_mess = chat_text(data) + "\nНЕДОСТАТОЧНО ДАННЫХ"
                    await dp.bot.send_message(chat_id, text=text_mess)
            else:
                my_adminset = db.get_user_access(user_role='admin')
                my_coorset = db.get_user_access(user_role='coordinator')
                if my_coorset:
                    my_adminset.extend(my_coorset)
                for y in range(len(my_adminset)):
                    chat_id = my_adminset[y][1]
                    text_mess = chat_text(data)
                    await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_coord_inline)
            db.add_dump_agent(send_to_dump(number_list[i], data))


# values получает словарь со всеми данными со статусом "Может работать" из Googlt sheets, разбивает на отдельные словари
# по ключу и отправляет каждый на проверку в search. Получает списки с номерами строк в таблице. Если длинна списка не 0,
# вызывает функцию отправки сообщения и записи в dump_agent (передает "порядковый номер" компании(int), список с
# номерами строк и данные словарем..
async def cheking_workbase():
    values_IM = google_search().get('ИЗИ МСК')
    values_Yg = google_search().get('ЯГО')
    values_Lk = google_search().get('Л КАРГО Мск')
    numbers_IM = column_comparison(values_IM)
    numbers_Yg = column_comparison(values_Yg)
    numbers_Lk = column_comparison(values_Lk)
    if len(numbers_IM) != 0:
        await cheking_list(1, numbers_IM, values_IM)
    if len(numbers_Yg) != 0:
        await cheking_list(2, numbers_Yg, values_Yg)
    if len(numbers_Lk) != 0:
        await cheking_list(3, numbers_Lk, values_Lk)