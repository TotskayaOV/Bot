from aiogram.types import Message
from loader import dp, db, log_id
from external_database import writing_pivot_table
from send_massage import notify


@dp.message_handler(commands=['pivot'])
async def up_pivot(message: Message, admin: bool):
    try:
        data = db.get_all_com_applications()
        writing_pivot_table(data)
        await message.answer(
            '<a href="https://docs.google.com/spreadsheets/d/1aJV1szm0CnChInO79eWrnrnxt6jsjmuFQ3tIDcVtbtY/edit#gid=0">'
            'Выгрузка Ok!</a>', parse_mode="HTML")
    except Exception as err:
        await message.answer('Ошибка выгрузки из БД в Googlesheets')
        notify(log_id, f"{err} :: ошибка выгрузки из БД в Googlesheets")
