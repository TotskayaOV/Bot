from loader import db, dp, log_id
from external_database import writing_status, writing_jira_status, google_update, rewriting_data
from send_massage import notify
from keyboards import kb_div_nd_inline, kb_coord_inline, kb_div_inline
from external_database import name_company_number
from .comment_area import update_agent_comment, call_admin, call_coor, call_div, call_all, \
    sent_to_com_applications, overwriting_comment, chat_text


def verification_agent(data: dict):
    """
    Ищет в рабочей ДБ агента по ИНН, получает кортеж, записывает в переменную info_from_dump в виде
    (id, name, phone, inn, company, datatime up, №row, comment). Отправляет сообщение формируя строку в переменную
    text_mes в call_coor(). Из info_from_dump получает id агента в рабочей БД и номер строки в Googlesheets.
    Через sent_to_com_applications() формирует словарь для записи в БД выполненных заявок. Через id_агента удаляет
    данные из рабочей БД. Через name_company_number получает номер компании.
    Проставляет статус "Активирован" через writing_status()
    text_wdb: {'agent_name': str, 'phone_number': int, 'inn_number': int, 'company_name': str, 'date_up': str,
    'date_down': str, 'comment': str}
    :param data: словарь {'ФИО': str, 'Телефон': str, 'ИНН': str, 'Компания': str}
    :return:
    """
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nверифицирован 🍌'
            call_coor(text_mes)
            id_agent_dump = info_from_dump[0]
            text_wdb = sent_to_com_applications(info_from_dump, data.get('last_user'))
            num_row = info_from_dump[6]
            db.remove_dump_agent(id_agent_dump)
            db.add_com_applications(text_wdb)
            num_table = name_company_number(text_wdb.get('company_name'))
            writing_status(str(num_row), num_table)
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(data.get('last_user'), 'Хватит тыкать!')
        notify(log_id, f"{db.get_user_access(user_id=data.get('last_user'))[0][2]} "
                       f"затыкивает верифицированного: {data.get('ФИО')} 🤬\n{err}")


def div_cancel_agent(data: dict):
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            try:
                info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            except:
                info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nотказ от сотрудничества 💩'
            call_div(text_mes)
            id_agent_dump = info_from_dump[0]
            text_wdb = sent_to_com_applications(info_from_dump, data.get('last_user'))
            text_wdb['comment'] = overwriting_comment(text_wdb.get('comment'), 'отказ от сотрудничества')
            num_row = info_from_dump[6]
            db.add_com_applications(text_wdb)
            db.remove_dump_agent(id_agent_dump)
            num_table = name_company_number(text_wdb.get('company_name'))
            writing_jira_status(str(num_row), num_table)
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(data.get('last_user'), f"Сотрудник {data.get('ФИО')} уже исключен из рабочих данных 🤫")
        notify(log_id, f"{data.get('last_user')} повторное нажатие кнопки {data.get('ФИО')}\n{err}")


def div_jira_agent(data: dict):
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
                info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            else:
                info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nJIRA 🤓'
            call_div(text_mes)
            id_agent_dump = info_from_dump[0]
            text_wdb = sent_to_com_applications(info_from_dump, data.get('last_user'))
            text_wdb['comment'] = overwriting_comment(text_wdb.get('comment'), 'JIRA')
            num_row = info_from_dump[6]
            db.add_com_applications(text_wdb)
            db.remove_dump_agent(id_agent_dump)
            num_table = name_company_number(text_wdb.get('company_name'))
            writing_jira_status(str(num_row), num_table)
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(data.get('last_user'), f"Сотрудник {data.get('ФИО')} уже исключен из рабочих данных 🤫")
        notify(log_id, f"{data.get('last_user')} повторное нажатие кнопки {data.get('ФИО')}\n{err}")


async def div_update_agent(data: dict):
    """

    :param last_user:
    :param data:
    :return:
    """
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
                info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            else:
                info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nданные обновлены 🤓'
            call_div(text_mes)
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
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(data.get('last_user'), f"Сотрудник уже исключен из рабочих данных 🤫")
        notify(log_id, f"{data.get('last_user')} повторное нажатие кнопки обновления данных\n{err}")


async def add_new_comment(data: dict, last_user: int):
    """
    Через add_dump_comm обновляет комментарий в БД агентов в работе. Формирует лист с id пользователей через
    get_user_access и циклом for перебирает их, отправляя сообщение с text_mess (формируется из agent_data от
    get_dump_agent, поиск по ИНН)
    :param last_user:
    :param data: {'inn_number': '(ИНН)', 'comment': 'сотрудничает с (название компании)'}
    :return: dp.bot.send_message
    """
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            if data.get('inn_number', False):
                agent_data = db.get_dump_agent(inn_number=data.get('inn_number'))[0]
                data['comment'] = overwriting_comment(agent_data[7], data.get('comment'))
                db.add_dump_comm(data)
            else:
                agent_data = db.get_dump_agent(phone_number=data.get('phone_number'))[0]
                data['comment'] = overwriting_comment(agent_data[7], data.get('comment'))
                db.add_dump_comm_phone(data)
            db.add_dump_comm(data)
            my_adminset = db.get_user_access(user_role='admin')
            my_divset = db.get_user_access(user_role='divisional_mentor')
            if my_divset:
                my_adminset.extend(my_divset)
            text_mess = f"ФИО: {agent_data[1]}\nТелефон: {agent_data[2]}\nИНН: {agent_data[3]}\n" \
                        f"Компания: {agent_data[4]}\n{data.get('comment')}"
            for y in range(len(my_adminset)):
                chat_id = my_adminset[y][1]
                if data.get('comment').endswith('ошибка в номере телефона') \
                        or data.get('comment').endswith('ошибка в номере ИНН'):
                    await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_nd_inline)
                else:
                    await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_inline)
            call_coor(f"ФИО: {agent_data[1]} отправлен на уточнение")
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(last_user, f'Сотрудник с ИНН {data.get("inn_number")} отсутствует в работе')
        call_admin(f"{db.get_user_access(user_id=last_user)[0][2]} "
                   f"пытается сломать бота через ИНН: {data.get('inn_number')} 🤬\n{err}")


def duplication_TIN_information(agent_tuples: list):
    string_message = ''
    for i_dict in range(len(agent_tuples)):
        string_message += f'{agent_tuples[i_dict][1]} т.: {agent_tuples[i_dict][2]} ' \
                          f'ИНН: {agent_tuples[i_dict][2]} Компания: {agent_tuples[i_dict][3]}\n'
    string_message += '🆘ДАННЫЕ ИНН ДУБЛИРУЮТСЯ🆘'
    call_all(string_message)
