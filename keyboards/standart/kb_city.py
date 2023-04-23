from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .kb_cancel_fsm import btn_cancel

kb_choosing_city = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_moskow = KeyboardButton(text='Москва')
btn_kasan = KeyboardButton(text='Казань')
btn_piter = KeyboardButton(text='Санкт-Петербург')


kb_choosing_city.add(btn_moskow, btn_kasan, btn_piter)
kb_choosing_city.add(btn_cancel)
