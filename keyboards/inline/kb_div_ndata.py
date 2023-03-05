from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import example_data

kb_div_nd_inline = InlineKeyboardMarkup(row_width=2)

btn_cancel_agent = InlineKeyboardButton(text='Не будет сотрудничать ⛔️', callback_data=example_data.new(move='cancel_agent'))
btn_update = InlineKeyboardButton(text='Данные обновлены ✅', callback_data=example_data.new(move='agent_update'))

kb_div_nd_inline.row(btn_cancel_agent, btn_update)
