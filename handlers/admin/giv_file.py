from aiogram.types import Message, InputFile
from loader import dp, db, log_id
from excel_worker import uploading_file
from send_massage import notify
import os


@dp.message_handler(commands=['excel'])
async def up_excel(message: Message, admin: bool):
    if admin:
        try:
            data = db.get_all_com_applications()
            data2 = db.get_all_comment_to_repository()
            uploading_file(data, data2)
            path = 'pivot.xlsx'
            await message.answer_document(InputFile(path))
            os.remove(path)
        except Exception as err:
            await message.answer('Ошибка выгрузки из БД')
            notify(log_id, f"{err} :: ошибка выгрузки из БД")
    else:
        await message.answer('У вас нет доступа к этой функции')