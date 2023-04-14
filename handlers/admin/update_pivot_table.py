from aiogram.types import Message
from loader import dp, db
from external_database import writing_pivot_table
@dp.message_handler(commands=['pivot'])
async def up_pivot(message: Message, admin: bool):
    print('Зашли в функцию')
    data = db.get_all_com_applications()
    print(data)
    writing_pivot_table(data)
