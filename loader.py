import os
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from working_database import DataBase
from config import db_path

memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=memory)
db = DataBase(db_path=db_path)

async def on_startup(_):
    print('Bot started!')
    try:
        db.create_table_com_applications()
        db.create_table_user_access()
        db.create_table_dump_agent()
        print('DataBase...ok!')
    except sqlite3.OperationalError:
        print('DataBase .... фиг вам, а не датабаза')

async  def on_shutdown(_):
    db.disconnect()

