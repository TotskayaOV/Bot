from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


btn_start = KeyboardButton('/start')


kb_menu.add(btn_start)
