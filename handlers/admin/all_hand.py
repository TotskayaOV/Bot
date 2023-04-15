from asyncio import sleep
from datetime import datetime

from aiogram.types import Message

from loader import dp, log_id
from working import cheking_workbase
from send_massage import notify


@dp.message_handler(commands=['remove'])
async def mes_start(message: Message, admin: bool):
    restart = False
    sleep_time = 60
    while restart == False:
        try:
            print(f'Запустились {datetime.now()}')
            await cheking_workbase()
            sleep_time = 60
        except Exception as err:
            notify(log_id, f"{err}\n:: {datetime.now()} ::\nошибка подключения к Googlesheets")
            sleep_time += 30
        finally:
            print(f'Уснули {datetime.now()}')
            await sleep(sleep_time)

