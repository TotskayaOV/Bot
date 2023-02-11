import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def change_digit():
    global btn_digit
    global kb_digit
    btn_digit = KeyboardButton(f'{random.randint(0, 100)}')
    kb_digit.add(btn_digit)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_help = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_digit = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

btn_start = KeyboardButton('/start')
btn_help = KeyboardButton('/help')
btn_digit = KeyboardButton(f'{random.randint(0, 100)}')
btn_location = KeyboardButton('Где я?', request_location=True)
btn_whoo = KeyboardButton('Кто я?', request_contact=True)

kb_menu.add(btn_help).add(btn_digit)
kb_help.add(btn_start, btn_digit, btn_location, btn_whoo)
kb_digit.add(btn_digit)