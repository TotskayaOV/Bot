import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from working_database import DataBase
from config import db_path
from send_massage import notify

memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=memory)
db = DataBase(db_path=db_path)
log_id = os.getenv('LOG_ID')
admin_id = os.getenv('GROUP_ID')


async def on_startup(_):
    notify(log_id, 'Bot started!')
    try:
        db.create_table_com_applications()
        db.create_table_user_access()
        db.create_table_dump_agent()
        db.create_list_mentors()
        db.create_table_dump_comment()
        notify(log_id, 'DataBase...ok!')
    except sqlite3.OperationalError:
        notify(log_id, 'DataBase .... фиг вам, а не датабаза')


async def on_shutdown(_):
    db.disconnect()

