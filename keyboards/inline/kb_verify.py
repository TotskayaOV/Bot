from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from call_back import example_data

kb_coord_inline = InlineKeyboardMarkup(row_width=2)

btn_verify = InlineKeyboardButton(text='Верифицирован', callback_data=example_data.new(name='olga'))

kb_coord_inline.row(btn_verify)