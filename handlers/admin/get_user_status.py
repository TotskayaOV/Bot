from aiogram.types import Message
from loader import dp, db


@dp.message_handler(commands=['show_users'])
async def show_users(message: Message, admin: bool):
    if admin:
        list_db = db.get_all_user_access()
        string_db = ""
        for i in range(len(list_db)):
            string_db += f'{list_db[i][2]}: id{list_db[i][1]}, роль - {list_db[i][3]}\n'
        await message.answer(text=string_db)
    else:
        await message.answer('У вас нет доступа к этой функции')
