from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import example_data

kb_coord_inline = InlineKeyboardMarkup(row_width=2)

btn_verify = InlineKeyboardButton(text='Верифицирован', callback_data=example_data.new(move='verif'))
btn_banan = InlineKeyboardButton(text='Другая компания', callback_data=example_data.new(move='banan'))

kb_coord_inline.row(btn_verify, btn_banan)