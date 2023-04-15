import datetime
from loader import db, dp
from send_massage import notify
from keyboards import kb_coord_inline
from keyboards import kb_div_nd_inline


def call_admin(text_mess: str):
    """
    Отправляет простое сообщение пользователям с ролью admin через notify
    :param text_mess: текстовое сообщение (str)
    """
    my_adminset = db.get_user_access(user_role='admin')
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)


def call_coor(text_mess: str):
    """
    Отправляет простое сообщение пользователям с ролью admin и coordinator через notify
    :param text_mess: текстовое сообщение (str)
    """
    my_adminset = db.get_user_access(user_role='admin')
    my_coorset = db.get_user_access(user_role='coordinator')
    if my_coorset:
        my_adminset.extend(my_coorset)
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)


def call_div(text_mess: str):
    """
    Отправляет простое сообщение пользователям с ролью admin и divisional_mentor через notify
    :param text_mess: текстовое сообщение (str)
    """
    my_adminset = db.get_user_access(user_role='admin')
    my_divset = db.get_user_access(user_role='divisional_mentor')
    if my_divset:
        my_adminset.extend(my_divset)
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)


def update_agent_comment(data: tuple, new_data: dict):
    """
    перезаписывает комментарий в БД агентов в работе
    :param data: (id, 'ФИО', телефон, ИНН, компания, время записи, № строки, комментарий)
    :param new_data: {'agent_name': ", 'phone_number': '', 'inn_number': '', 'role': '', 'company_name': ''}
    :return:
    """
    comment = overwriting_comment(data[7], 'данные обновлены')
    writing_dict = {'agent_name': new_data.get('agent_name'), 'phone_number': new_data.get('phone_number'),
                    'inn_number': new_data.get('inn_number'), 'comment': comment, 'id': data[0]}
    db.update_dump_comm(writing_dict)


def overwriting_comment(comment: str, additional_comment: str):
    if comment == "":
        new_comment = additional_comment
    else:
        new_comment = comment + ', ' + additional_comment
    return new_comment


def sent_to_com_applications(agent_set: tuple, user_id: int):
    """
    :param user_id:
    :param agent_set: кортеж в виде (id, agent_name, phone_number, inn_number, company_name, date_up,
                    row_number, comment)
    :return: dict: {'agent_name': str, 'phone_number': int, 'inn_number': int, 'company_name': str, 'date_up': str,
    'date_down': str, 'comment': str}
    """
    dt_obj = datetime.datetime.now()
    data_dict = {'agent_name': agent_set[1], 'phone_number': agent_set[2], 'inn_number': agent_set[3],
                 'company_name': agent_set[4], 'date_up': agent_set[5],
                 'date_down': dt_obj.strftime("%Y-%m-%d %H:%M:%S"), 'comment': agent_set[7], 'last_user': user_id}
    return data_dict


def chat_text(data: dict):
    """
    Формирует строку для отправки сообщения
    :param data: принимает словарь в котором должны содержаться ключи:agent_name, phone_number, inn_number, company_name
    :return: строка (str)
    """
    text_mess = f"ФИО:{data.get('agent_name')}\nТелефон: {data.get('phone_number')}\n" \
                f"ИНН:{data.get('inn_number')}\nКомпания: {data.get('company_name')}\n" \
                f"Роль: {data.get('role')}"
    return text_mess


def send_to_dump(row_number: int, data: dict):
    """
    Формирует словарь для записи в ДБ (таблица агенты в работе - dump_agent)
    :param row_number: номер строки в Google sheets
    :param data: {'agent_name', 'phone_number', 'inn_number', 'company_name', 'date_up',
    'row_number': row_number, 'comment'}
    'date_up' - время исполения функции
    """
    dt_obj = datetime.datetime.now()
    dump_data = {'agent_name': data.get('agent_name'), 'phone_number': data.get('phone_number'),
                 'inn_number': data.get('inn_number'), 'company_name': data.get('company_name'),
                 'date_up': dt_obj.strftime("%Y-%m-%d %H:%M:%S"), 'row_number': row_number, 'comment': ''}
    return dump_data


async def sent_div_list(data):
    """
    Функция для отправки сообщения админам и ДН. Формирует список с id_user роль-дивизионный_менеджер и объединяет
    его с my_adminset. Циклом for проходит по id_user общего списка и отправляет сообщение сформировав строку через
    chat_text(). К сообщению прикрепляется инлайн клавиатура kb_div_nd_inline.
    :param data: словарь {'agent_name': '', 'phone_number': '', 'inn_number': '', 'role': '', 'company_name': ''}
    """
    my_adminset = db.get_user_access(user_role='admin')
    my_divset = db.get_user_access(user_role='divisional_mentor')
    if my_divset:
        my_adminset.extend(my_divset)
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        text_mess = chat_text(data) + "\nНЕДОСТАТОЧНО ДАННЫХ"
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_nd_inline)


async def sent_coor_list(data):
    """
    Функция для отправки сообщения админам и ДН. Формирует список с id_user роль-координатор и объединяет
    его с my_adminset. Циклом for проходит по id_user общего списка и отправляет сообщение сформировав строку через
    chat_text(). К сообщению прикрепляется инлайн клавиатура kb_coord_inline.
    :param data: словарь {'agent_name': '', 'phone_number': '', 'inn_number': '', 'role': '', 'company_name': ''}
    """
    my_adminset = db.get_user_access(user_role='admin')
    my_coorset = db.get_user_access(user_role='coordinator')
    if my_coorset:
        my_adminset.extend(my_coorset)
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        text_mess = chat_text(data)
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_coord_inline)
