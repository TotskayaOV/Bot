from aiogram.types import Message
from loader import dp, db


def string_kick_tasks():
    """
    формирует строку из списка кортежей оповещений по запросу в базу данных
    :return: нумерованная строка с id, временем и группой пользователей (для рассылки)
    """
    list_db = db.get_all_task_kick()
    string_db = "Сейчас отслеживаются:\n"
    if len(list_db) > 0:
        numder_list = 1
        for i in range(len(list_db)):
            string_db += f'{numder_list}. id оповещения в базе: {list_db[i][0]}\n' \
                         f'время {list_db[i][1]},\n' \
                         f'группа: {list_db[i][2]}'
            numder_list += 1
    else:
        string_db += "\nсписок оповещения пуст 😎"
    return string_db


@dp.message_handler(commands=['kick_tasks'])
async def show_kick(message: Message, admin: bool):
    if admin:
        string_db = string_kick_tasks()
        await message.answer(text=string_db)
    else:
        await message.answer('У вас нет доступа к этой функции')
