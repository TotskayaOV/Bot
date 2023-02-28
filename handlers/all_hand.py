from loader import dp, db
from aiogram.types import Message
from working import cheking_workbase

@dp.message_handler(commands=['remove'])
async def mes_start(message: Message):
    await cheking_workbase()
