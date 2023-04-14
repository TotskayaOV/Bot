from asyncio import sleep
from datetime import datetime

from aiogram.types import Message

from loader import dp
from working import cheking_workbase


@dp.message_handler(commands=['remove'])
async def mes_start(message: Message, admin: bool):
    print('Зашли в функцию')
    restart = False
    while restart == False:
        print(f'Запустились {datetime.now()}')
        await cheking_workbase()
        print(f'Уснули {datetime.now()}')
        await sleep(60)
