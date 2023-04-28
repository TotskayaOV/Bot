from loader import db, log_id
from external_database import writing_status, writing_jira_status, google_update, rewriting_data
from send_massage import notify
from external_database import name_company_number
from .comment_area import update_agent_comment, call_admin, call_coor, call_div, call_all, \
    sent_to_com_applications, overwriting_comment, sent_div_list, sent_coor_list
from .using_comments_db import get_comments_db
from .checking_progress import writing_table_task_progress


def verification_agent(data: dict):
    """
    Метод, обрабатывающий ответ о верификации агента:
        Проверяет количество записей в задачах в работе по длинне списка из запроса в БД. Если список
        превышает 1, то передает общее сообщение о наличии двух записей с одним ИНН через duplication_TIN_information()

        Ищет в рабочей ДБ агента по ИНН, получает кортеж, записывает в переменную info_from_dump в виде
        (id, name, phone, inn, company, datatime up, №row, comment).

        Отправляет сообщение формируя строку в переменную text_mes в call_coor().

        Из info_from_dump получает id агента в рабочей БД и номер строки в Googlesheets.

        Через sent_to_com_applications() формирует словарь для записи в БД выполненных заявок:
        text_wdb: {'agent_name': str, 'phone_number': int, 'inn_number': int, 'company_name': str, 'date_up': str,
        'date_down': str, 'comment': str}

        С помощью id_агента удаляет данные из рабочей БД remove_dump_agent и из БД оповещений remove_task_kick()

        С помощью name_company_number получает номер компании.

        Проставляет статус "Активирован" через writing_status(номер строки, номер компании)
    :param data: словарь {'ФИО': str, 'Телефон': str, 'ИНН': str, 'Компания': str}
    """
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nверифицирован 🍌'
            call_coor(text_mes)
            id_agent_dump = info_from_dump[0]
            text_wdb = sent_to_com_applications(info_from_dump, data.get('last_user'))
            num_row = info_from_dump[6]
            db.remove_task_kick(id_agent_dump)
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
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nотказ от сотрудничества'
            call_div(text_mes)
            get_comments_db(info_from_dump, data.get('last_user'), 'отказ от сотрудничества')
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
            get_comments_db(info_from_dump, data.get('last_user'), 'JIRA')
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
    Обрабатывает сообщение от группы с ролью дивизионный-наставник:
        Проверяет количество записей в задачах в работе по длинне списка из запроса в БД. Если список
        превышает 1, то передает общее сообщение о наличии двух записей с одним ИНН через duplication_TIN_information()

        Делает попытку запроса в БД для поиска записи по ИНН. Если попытка не удалась, делает запрос по номеру
        телефона

        Формирует ответ бота на действие в виде простого сообщения через call_div()

        Через get_comments_db() обновляет комментарий в задачах в работе БД

        Через метод rewriting_data обновляет данные из Google sheets и проверяет их на полноту. Если данные не полные
        возвращает сообщение с комментарием о недостаточности данных, если полные добавляет в отслеживание задачу и
        передает  в sent_coor_list полученный словарь с данными агента

    :param data: словарь сформированный callback сообщением с идентификатором простаившего его пользователя
    :return: sent_coor_list(dict)
    """
    try:
        if len(db.get_dump_agent(inn_number=data.get('ИНН'))) < 2:
            if len(db.get_dump_agent(inn_number=data.get('ИНН'))) == 1:
                info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
            else:
                info_from_dump = db.get_dump_agent(phone_number=data.get('Телефон'))[0]
            text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nданные обновлены 🤓'
            call_div(text_mes)
            get_comments_db(info_from_dump, data.get('last_user'), 'данные обновлены')
            num_row = info_from_dump[6]
            num_table = name_company_number(info_from_dump[4])
            value = rewriting_data(num_table, num_row, google_update(str(num_row), num_table))
            update_agent_comment(info_from_dump, value)
            if (value.get('inn_number') == '') or (value.get('phone_number') == ''):
                await sent_div_list(value, 'НЕДОСТАТОЧНО ДАННЫХ', 1)
            else:
                writing_table_task_progress(value, 1)
                await sent_coor_list(value)
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
                get_comments_db(agent_data, last_user, data['comment'])
                data['comment'] = overwriting_comment(agent_data[7], data.get('comment'))
                db.add_dump_comm(data)
            else:
                agent_data = db.get_dump_agent(phone_number=data.get('phone_number'))[0]
                get_comments_db(agent_data, last_user, data['comment'])
                data['comment'] = overwriting_comment(agent_data[7], data.get('comment'))
                db.add_dump_comm_phone(data)
            db.add_dump_comm(data)
            db.remove_task_kick(agent_data[0])
            if data.get('comment').endswith('ошибка в номере телефона')\
                    or data.get('comment').endswith('ошибка в номере ИНН'):
                await sent_div_list(agent_data, data.get('comment'), 1)
            else:
                await sent_div_list(agent_data, data.get('comment'), 2)
            call_coor(f"ФИО: {agent_data[1]} отправлен на уточнение")
        else:
            duplication_TIN_information(db.get_dump_agent(inn_number=data.get('ИНН')))
    except Exception as err:
        notify(last_user, f'Сотрудник с ИНН {data.get("inn_number")} отсутствует в работе')
        call_admin(f"{db.get_user_access(user_id=last_user)[0][2]} "
                   f"пытается сломать бота через ИНН: {data.get('inn_number')} 🤬\n{err}")


def duplication_TIN_information(agent_tuples: list):
    """
    формирует текст сообщения об ошибке данных и наличии дубликатов ИНН у разных агентов
    :param agent_tuples: список кортежей из БД с данными агентов с одинаковыми ИНН
    :return: call_all(текст сообщения в формате str)
    """
    string_message = ''
    for i_dict in range(len(agent_tuples)):
        string_message += f'{agent_tuples[i_dict][1]} т.: {agent_tuples[i_dict][2]} ' \
                          f'ИНН: {agent_tuples[i_dict][4]} Компания: {agent_tuples[i_dict][3]}\n'
    string_message += '🆘ДАННЫЕ ИНН ДУБЛИРУЮТСЯ🆘'
    call_all(string_message)
