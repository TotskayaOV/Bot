from external_database import *
from datetime import datetime
from asyncio import sleep
from loader import db, log_id
from send_massage import notify
from .comment_area import sent_div_list, sent_coor_list, send_to_dump, update_agent_comment


async def storage_defective_agents(defective_list: list):
    await sleep(60)
    try:
        for element in defective_list:
            up_data = rewriting_data(element[0], element[1],
                                     google_update(element[1], element[0]))
            if (up_data.get('inn_number') == '') or (up_data.get('phone_number') == ''):
                await sent_div_list(up_data)
            else:
                if len(db.get_dump_agent(inn_number=up_data.get('inn_number'))) == 1:
                    update_agent_comment(db.get_dump_agent(inn_number=up_data.get('inn_number'))[0], up_data)
                else:
                    update_agent_comment(db.get_dump_agent(phone_number=up_data.get('phone_number'))[0], up_data)
                await sent_coor_list(up_data)
        defective_list.clear()
    except Exception as err:
        notify(log_id, f"{err}\n:: {datetime.now()} ::\nошибка подключения к Googlesheets "
                       f"при обновлении storage_defective_agents")


async def cheking_list(num_com: int, number_list: list, values: dict):
    """
    Проходит циклом for по индексам(i) полученного списка строк(number_list). Через функцию writing_data формирует
    карточку агента в виде словаря.
    Проверяет наличие этого агента по ФИО через get_dump_agent среди тех, кто уже находится в работе. Если его там нет,
    проверяет карточку на полноту данных (ИНН и телефон). Если данные не полные, то уходит в сон через sleep из asyncio
    на 60 секунд. После этого повторно проверяет этого же агента на полноту данных.
    Если данные не полные запускает sent_div_list()
    Если данные полные, то переприсваивает data и запускает sent_coor_list().
    :param num_com: заданный номер компании (int) - не используется внутри метода, передается в методы внутри
    :param number_list: список с номерами строк агентов для работы (list[int])
    :param values: данные для формирования карточки агента (через writing_data)
    :return: записывает данные в БД агентов в работе
    """
    list_for_defective_agents = []
    for i in range(len(number_list)):
        data = writing_data(num_com, number_list[i], values)
        check_dump = db.get_dump_agent(agent_name=data.get('agent_name'))
        if not check_dump:
            if (data.get('inn_number') == '') or (data.get('phone_number') == ''):
                list_for_defective_agents.append([num_com, number_list[i]])
            else:
                await sent_coor_list(data)
            db.add_dump_agent(send_to_dump(number_list[i], data))
    if len(list_for_defective_agents) != 0:
        await storage_defective_agents(list_for_defective_agents)
        list_for_defective_agents.clear()


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
    elif len(numbers_Yg) != 0:
        await cheking_list(2, numbers_Yg, values_Yg)
    elif len(numbers_Lk) != 0:
        await cheking_list(3, numbers_Lk, values_Lk)
    elif len(numbers_LkSpb) != 0:
        await cheking_list(4, numbers_LkSpb, values_LkSpb)
    elif len(numbers_IS) != 0:
        await cheking_list(5, numbers_IS, values_IS)
    elif len(numbers_IK) != 0:
        await cheking_list(6, numbers_IK, values_IK)
