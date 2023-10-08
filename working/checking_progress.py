from asyncio import sleep
from datetime import datetime, timedelta

from loader import db
from .comment_area import call_coor



def writing_table_task_progress(dict_agent: dict, type_num: int):
    """
    Добавляет запись в таблицу для отслеживания выполнения задач координаторами
    (заранее заложен параметр, по которому в дальнейшем можно сортировать кому нужно напомнить о задаче)
    :param dict_agent: словарь с данными из таблицы задач в работе
    :param type_num: параметр, определяющий группу получателей (1 - координаторы)
    :return:
    """
    id_new_task = db.get_dump_agent(agent_name=dict_agent.get('agent_name'))[0]
    dt_obj = datetime.now()
    db.add_task_kick({'id_task': id_new_task[0],
                      'message_time': dt_obj.strftime("%d-%m-%Y %H:%M:%S"),
                     'count_kick': type_num})


async def checking_tasks_progress():
    """
    Бесконечно проверяет таблицу с данными для оповещения о завсших в работе задачах раз в минуту.
    Если в таблице есть данные, передает в функцию проверки времени. Останавливается на 1 минуту после передачи.
    """
    loop_variable = True
    while loop_variable:
        check_kick = db.get_all_task_kick()
        if not check_kick:
            await sleep(60)
        else:
            checking_time(check_kick)
            await sleep(60)


def checking_time(kicks_tuples: list):
    """
    Проверяет список задач. В зависимости от времени нахождения в списке задач отправляет сообщение и, в случае
    необходмиости, удаляет задачу из списка
    :param kicks_tuples: [(int(id), datetime, int(count)), ].
    """
    reference_point = datetime.now()
    for elem in kicks_tuples:
        hanging_time = reference_point - datetime.strptime(elem[1], "%d-%m-%Y %H:%M:%S")
        if timedelta(minutes=6) >= hanging_time >= timedelta(minutes=5):
            name_agent = db.get_dump_agent(id=elem[0])[0]
            call_coor(f'‼️Внимание, заявка необработана уже более 5 минут. Возьмите в работу {name_agent[1]}️')
            db.update_task_kick({'count_kick': 1, 'id_task': elem[0]})
        elif hanging_time >= timedelta(minutes=10):
            call_coor('‼️‼️‼️‼️Внимание, есть необработанная заявка!Возьмите в работу')
            db.remove_task_kick(elem[0])

