from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import cancel_agent_div

kb_div_nd_inline = InlineKeyboardMarkup(row_width=2)

btn_cancel_agent = InlineKeyboardButton(text='Не будет сотрудничать ⛔️', callback_data=cancel_agent_div.new(cancel_agent='cancel_agent'))
btn_update = InlineKeyboardButton(text='Данные обновлены ✅', callback_data=cancel_agent_div.new(cancel_agent='agent_update'))

kb_div_nd_inline.row(btn_cancel_agent, btn_update)
