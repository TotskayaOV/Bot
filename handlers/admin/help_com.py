from aiogram.types import Message
from loader import dp


@dp.message_handler(commands=['help'])
async def show_users(message: Message, admin: bool):
    if admin:
        string_db = "команды:\n/remove - запуск обновления\n/pivot - выгрузка\n/current_tasks - задачи в работе\n" \
                    "/add - добавить нового пользователя(нужен id)\n/show_users - показать список пользователей\n" \
                    "/del - удалить пользователя(нужен id)\n /del_dump - удаление задачи из работы\n" \
                    "/stop - остановка обновления"
        await message.answer(text=string_db)
    else:
        await message.answer('Обратитесь за помощью к администратору')
