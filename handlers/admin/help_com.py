from aiogram.types import Message
from loader import dp, admin_id


@dp.message_handler(commands=['help'])
async def show_users(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        string_db = "команды:\n/remove - запуск обновления\n/excel - выгрузка (файл excel)\n" \
                    "/current_tasks - задачи в работе\n" \
                    "/add - добавить нового пользователя(нужен id)\n/show_users - показать список пользователей\n" \
                    "/del - удалить пользователя(нужен id)\n /del_dump - удаление задачи из работы"
        await message.answer(text=string_db)
    else:
        await message.answer('Обратитесь за помощью к администратору')
