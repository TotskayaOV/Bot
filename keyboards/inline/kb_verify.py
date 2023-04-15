from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import other_company

kb_coord_inline = InlineKeyboardMarkup(row_width=4)

btn_verify = InlineKeyboardButton(text='Верифицирован 😏', callback_data=other_company.new(verif='verif'))
btn_banana = InlineKeyboardButton(text='Другая компания 😡', callback_data=other_company.new(verif='banana'))
btn_inn_error = InlineKeyboardButton(text='Ошибка в ИНН 🤬', callback_data=other_company.new(verif='error_inn_data'))
btn_phone_error = InlineKeyboardButton(text='Ошибка в телефоне 🤬',
                                       callback_data=other_company.new(verif='error_phone_data'))

kb_coord_inline.add(btn_verify, btn_banana)
kb_coord_inline.add(btn_inn_error, btn_phone_error)
