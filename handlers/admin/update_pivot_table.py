from aiogram.types import Message
from loader import dp, db, log_id
from external_database import writing_pivot_table
from send_massage import notify


@dp.message_handler(commands=['pivot'])
async def up_pivot(message: Message, admin: bool):
    try:
        data = db.get_all_com_applications()
        writing_pivot_table(data)
    except Exception as err:
        notify(log_id, f"{err} :: ошибка выгрузки из БД в Googlesheets")
