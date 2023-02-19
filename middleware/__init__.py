from aiogram import Dispatcher
from .mw_dbase import AddUserRole

def setup(dp: Dispatcher):
    dp.middleware.setup(AddUserRole())