from aiogram.types import Message
from loader import dp, db


def string_current_tasks():
    """
    формирует строку из списка котрежей задач в работе
    :return: нумерованная строка задач в работе, содержит ФИО, id(PKey), название компании, телефон, ИНН,
            время создания заявки и все комментарии
    """
    list_db = db.get_all_dump_agent()
    string_db = "Сейчас в работе:\n"
    if len(list_db) > 0:
        numder_list = 1
        for i in range(len(list_db)):
            string_db += f'{numder_list}. {list_db[i][1]}: id задачи в базе {list_db[i][0]}\n' \
                         f'Компания {list_db[i][4]},\n' \
                         f'телефон: {list_db[i][2]}, ИНН: {list_db[i][3]},\n' \
                         f'время создания заявки: {list_db[i][5]}\n' \
                         f'комментарий: {list_db[i][7]}\n'
            numder_list += 1
    else:
        string_db += "\nсписок ожидания пуст 😎"
    return string_db


@dp.message_handler(commands=['current_tasks'])
async def show_tasks(message: Message, admin: bool):
    if admin:
        string_db = string_current_tasks()
        await message.answer(text=string_db)
    else:
        await message.answer('У вас нет доступа к этой функции')
