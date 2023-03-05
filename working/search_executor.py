from external_database import *
import datetime
from loader import db, dp
from keyboards import kb_coord_inline
from keyboards import kb_div_nd_inline
import time


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
    :param data: {'agent_name', 'phone_number', 'inn_number', 'company_name', 'date_up', 'row_number': row_number, 'comment'}
    'date_up' - время исполения функции
    """
    dump_data = {'agent_name': data.get('agent_name'), 'phone_number': data.get('phone_number'),
                 'inn_number': data.get('inn_number'), 'company_name': data.get('company_name'),
                 'date_up': datetime.datetime.now(), 'row_number': row_number, 'comment': ''}
    return dump_data


async def sent_div_list(data, my_adminset):
    my_divset = db.get_user_access(user_role='divisional_mentor')
    if my_divset:
        my_adminset.extend(my_divset)
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        text_mess = chat_text(data) + "\nНЕДОСТАТОЧНО ДАННЫХ"
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_nd_inline)

async def sent_coor_list(data, my_adminset):
    my_coorset = db.get_user_access(user_role='coordinator')
    if my_coorset:
        my_adminset.extend(my_coorset)
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        text_mess = chat_text(data)
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_coord_inline)

async def cheking_list(num_com: int, number_list: list, values: dict):
    """
    Проходит циклом for по индексам(i) полученного списка строк(number_list). Через функцию writing_data формирует
    карточку агента в виде словаря.
    Проверяет наличие этого агента по ФИО через get_dump_agent среди тех, кто уже находится в работе. Если его там нет,
    проверяет карточку на полноту данных (ИНН и телефон). Если данные не полные, то отправляет сообщене
    дивизионным наставникам и админам (списки с id_user my_divset и my_adminset).
    Если данные полные, то отправляет сообщение координаторам и админам (списки с id_user my_divset и my_coorset).
    В обоих случаех через if True проверяет есть ли в my_divset или my_coorset данные и в случае наличия объединает
    в один список с my_adminset.
    :param num_com: заданный номер компании (int) - не используется внутри метода, передается в методы внутри
    :param number_list: список с номерами строк агентов для работы (list[int])
    :param values: данные для формирования карточки агента (через writing_data)
    :return: передает карточку агента (str) сообщением в бота заданным пользователям, записывает данные в БД агентов
    в работе
    """
    for i in range(len(number_list)):
        data = writing_data(num_com, number_list[i], values)
        check_dump = db.get_dump_agent(agent_name=data.get('agent_name'))
        my_adminset = db.get_user_access(user_role='admin')
        if not check_dump:
            if (data.get('inn_number') == '') or (data.get('phone_number') == ''):
                time.sleep(60)
                up_data = rewriting_data(num_com, number_list[i], google_update(number_list[i], num_com))
                if (up_data.get('inn_number') == '') or (up_data.get('phone_number') == ''):
                    await sent_div_list(data, my_adminset)
                else:
                    data = up_data
                    await sent_coor_list(data, my_adminset)
            else:
                await sent_coor_list(data, my_adminset)
            db.add_dump_agent(send_to_dump(number_list[i], data))


async def cheking_workbase():
    """
    values получает словарь со всеми данными со статусом "Может работать" из Googlt sheets, разбивает на отдельные
    словари по ключу (название компании) и отправляет каждый на проверку в search.
    Получает список (list) с номерами строк (int) агентов для работы в таблице. Если длинна списка не 0, вызывает
    функцию отправки сообщения и записи в dump_agent (передает "порядковый номер" компании(int), список с номерами
    строк (list) и данные словарем (dict)
    """
    values_IM = google_search().get('ИЗИ МСК')
    values_Yg = google_search().get('ЯГО')
    values_Lk = google_search().get('Л КАРГО Мск')
    values_LkSpb = google_search().get('Л КАРГО Спб')
    values_IS = google_search().get('ИЗИ СПб')
    values_IK = google_search().get('ИЗИ Казань')
    numbers_IM = column_comparison(values_IM)
    numbers_Yg = column_comparison(values_Yg)
    numbers_Lk = column_comparison(values_Lk)
    numbers_LkSpb = column_comparison(values_LkSpb)
    numbers_IS = column_comparison(values_IS)
    numbers_IK = column_comparison(values_IK)
    if len(numbers_IM) != 0:
        await cheking_list(1, numbers_IM, values_IM)
    if len(numbers_Yg) != 0:
        await cheking_list(2, numbers_Yg, values_Yg)
    if len(numbers_Lk) != 0:
        await cheking_list(3, numbers_Lk, values_Lk)
    if len(numbers_LkSpb) != 0:
        await cheking_list(4, numbers_LkSpb, values_LkSpb)
    if len(numbers_IS) != 0:
        await cheking_list(5, numbers_IS, values_IS)
    if len(numbers_IK) != 0:
        await cheking_list(6, numbers_IK, values_IK)