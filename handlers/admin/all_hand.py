from asyncio import sleep
from datetime import datetime

from aiogram.types import Message

from loader import dp, log_id
from working import cheking_workbase
from send_massage import notify


@dp.message_handler(commands=['remove'])
async def mes_start(message: Message, admin: bool):
    if admin:
        restart = False
        sleep_time = 60
        while not restart:
            try:
                await cheking_workbase()
            except Exception as err:
                notify(log_id, f"{err}\n:: {datetime.now()} ::\nошибка подключения к Googlesheets\n{sleep_time}")
                sleep_time += 30
            else:
                sleep_time = 60
            finally:
                await sleep(sleep_time)


