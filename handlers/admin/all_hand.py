from asyncio import sleep
from datetime import datetime

from aiogram.types import Message

from loader import dp, log_id
from working import cheking_workbase, call_admin, checking_tasks_progress
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
                if sleep_time == 180:
                    call_admin('Всё окей 😉 Я пробился 😎 Работаем дальше 😇')
                sleep_time = 60
            finally:
                if sleep_time == 180:
                    call_admin('‼️‼️‼️Ошибка подключения к Googlesheets 👿‼️‼️‼️')
                await sleep(sleep_time)


