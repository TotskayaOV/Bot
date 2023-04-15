from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .kb_cancel_fsm import btn_cancel


kb_role_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_admin = KeyboardButton(text='admin')
btn_coor = KeyboardButton(text='coordinator')
btn_divmen = KeyboardButton(text='divisional_mentor')

kb_role_user.add(btn_admin, btn_coor, btn_divmen)
kb_role_user.add(btn_cancel)
