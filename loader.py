import os
import sqlite3

from aiogram import Bot, Dispatcher, types
# from external_database import GoogleTable

from working_database import DataBase
from config import db_path

# class FreakTelegramBot(Bot):
#     def __init__(
#             self,
#             token,
#             parse_mode,
#             google_table=None,):
#         super().__init__(token, parse_mode=parse_mode)
#         self.__google_table: GoogleTable = google_table
#
# bot: FreakTelegramBot = FreakTelegramBot(
#     token=os.getenv('TOKEN'),
#     parse_mode=types.ParseMode.HTML,
#     google_table=GoogleTable("cbt.json",
#                              "https://docs.google.com/spreadsheets/d/1ammlfHCNNYwT7TEMyilZxcAEsDUgA4VWcGfjAnEhL2g"))


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)
db = DataBase(db_path=db_path)

async def on_startup(_):
    print('Bot started!')
    try:
        db.create_table_com_applications()
        print('DataBase...ok!')
    except sqlite3.OperationalError:
        print('DataBase .... фиг вам, а не датабаза')

async  def on_shutdown(_):
    db.disconnect()

