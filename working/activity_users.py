from loader import db, dp
from datetime import datetime
from external_database import writing_status, writing_jira_status, google_update, rewriting_data
from send_massage import notify
from keyboards import kb_div_nd_inline, kb_coord_inline
from .search_executor import chat_text
from external_database import name_company_number
from .comment_area import update_agent_comment


def call_admin(text_mess: str):
    """
    Отправляет простое сообщение пользователям с ролью admin через notify
    :param text_mess: текстовое сообщение (str)
    :return:
    """
    my_adminset = db.get_user_access(user_role='admin')
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)

def call_div(text_mess: str):
    """
    Отправляет простое сообщение пользователям с ролью admin и divisional_mentor через notify
    :param text_mess: текстовое сообщение (str)
    :return:
    """
    my_adminset = db.get_user_access(user_role='admin')
    my_divset = db.get_user_access(user_role='divisional_mentor')
    if my_divset:
        my_adminset.extend(my_divset)
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)


def sent_to_com_applications(agent_set: set):
    """
    :param agent_set: множество в виде (id, agent_name, phone_number, inn_number, company_name, date_up,
                    row_number, comment)
    :return: dict
    """
    data_dict = {'agent_name': agent_set[1], 'phone_number': agent_set[2], 'inn_number': agent_set[3],
                 'company_name': agent_set[4], 'date_up': agent_set[5], 'date_down': datetime.now(),
                 'comment': agent_set[7]}
    return data_dict


# Получаем на вход данные типа dict: {'ФИО': 'Аннжелина Джоли', 'Телефон': ' 79333064959', 'ИНН': '972734238895', 'Компания': ' Л Карго Мск'}
# Из кортежа получаем id в dump (для последующего удаления), через функцию sent_to_com_applications формируем словарь
# для отправки в com_applications, получаем номер строки в которой нужно будет изменить статус
def verification_agent(data: dict) -> object:
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
            info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
        else:
            info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
        text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nверифицирован 🍌'
        call_div(text_mes)
        id_agent_dump = info_from_dump[0]
        text_wdb = sent_to_com_applications(info_from_dump)
        num_row = info_from_dump[6]
        db.remove_dump_agent(id_agent_dump)
        db.add_com_applications(text_wdb)
        num_table = name_company_number(text_wdb.get('company_name'))
        writing_status(str(num_row), num_table)
    except:
        call_admin(f"Затыкали {data.get('ФИО')} 🤬")

def div_cancel_agent(data: dict):
    try:
        print(data)
        info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
        text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nотказ от сотрудничества 💩'
        call_admin(text_mes)
        print(text_mes)
        id_agent_dump = info_from_dump[0]
        text_wdb = sent_to_com_applications(info_from_dump)
        temp_variable = text_wdb.get('comment')
        text_wdb['comment'] = temp_variable + ', отказ от сотрудничества'
        num_row = info_from_dump[6]
        db.add_com_applications(text_wdb)
        db.remove_dump_agent(id_agent_dump)
        num_table = name_company_number(text_wdb.get('company_name'))
        print(num_table)
        writing_jira_status(str(num_row), num_table)
    except:
        call_div(f"Сотрудник {data.get('ФИО')} уже исключен из рабочих данных 🤫")


def div_jira_agent(data: dict):
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
            info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
        else:
            info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
        text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nJIRA 🤓'
        call_div(text_mes)
        id_agent_dump = info_from_dump[0]
        text_wdb = sent_to_com_applications(info_from_dump)
        temp_variable = text_wdb.get('comment')
        text_wdb['comment'] = temp_variable + ', JIRA'
        num_row = info_from_dump[6]
        db.add_com_applications(text_wdb)
        db.remove_dump_agent(id_agent_dump)
        num_table = name_company_number(text_wdb.get('company_name'))
        writing_jira_status(str(num_row), num_table)
    except:
        call_div(f"Сотрудник {data.get('ФИО')} исключен из рабочих данных")


async def div_update_agent(data: dict):
    """

    :param data:
    :return:
    """
    if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
        info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
    else:
        info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
    text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nданные обновлены 🤓'
    call_admin(text_mes)
    num_row = info_from_dump[6]
    num_table = name_company_number(info_from_dump[4])
    value = rewriting_data(num_table, num_row, google_update(str(num_row), num_table))
    update_agent_comment(info_from_dump, value)
    my_adminset = db.get_user_access(user_role='admin')
    if (value.get('inn_number') == '') or (value.get('phone_number') == ''):
        my_divset = db.get_user_access(user_role='divisional_mentor')
        if my_divset:
            my_adminset.extend(my_divset)
        for y in range(len(my_adminset)):
            chat_id = my_adminset[y][1]
            text_mess = chat_text(value) + "\nНЕДОСТАТОЧНО ДАННЫХ"
            await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_nd_inline)
    else:
        my_coorset = db.get_user_access(user_role='coordinator')
        if my_coorset:
            my_adminset.extend(my_coorset)
        for y in range(len(my_adminset)):
            chat_id = my_adminset[y][1]
            text_mess = chat_text(value)
            await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_coord_inline)
