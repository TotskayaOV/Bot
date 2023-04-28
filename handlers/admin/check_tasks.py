from asyncio import sleep
from datetime import datetime

from aiogram.types import Message

from loader import dp, log_id
from working import cheking_workbase, call_admin, checking_tasks_progress
from send_massage import notify



@dp.message_handler(commands=['check_t'])
async def mes_check(message: Message, admin: bool):
    if admin:
        restart = False
        while not restart:
            try:
                await checking_tasks_progress()
            except Exception as err:
                notify(log_id, f"{err}\n:: {datetime.now()} ::\nошибка подключения к задачам")
