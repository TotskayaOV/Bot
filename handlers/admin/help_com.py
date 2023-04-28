from aiogram.types import Message
from loader import dp, admin_id


@dp.message_handler(commands=['help'])
async def show_users(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        string_db = "команды:\n/excel - выгрузка (файл excel)" \
                    "\n/unloading - выгрузка за период\n\n/current_tasks - задачи в работе\n" \
                    "/kick_tasks - показать список отслеживания\n" \
                    "/add - добавить нового пользователя(нужен id)\n/show_users - показать список пользователей\n" \
                    "/mentor - добавить наставника\n/show_mentors - показать список наставников\n" \
                    "/del - удалить пользователя (нужен id)\n" \
                    "/del_m - удалить наставника (нужен id)\n\n" \
                    "/del_dump - удаление задачи из работы\n/del_kick - удаление уведомления о невыполненной задачи" \
                    " (используется после удаления задачи из работы)\n" \
                    "/del_ca - удаление выполненной задачи (нужен id (см. выгрузку)"
        await message.answer(text=string_db)
    else:
        await message.answer('Обратитесь за помощью к администратору')
