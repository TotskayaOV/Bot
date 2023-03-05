from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import example_data

kb_div_inline = InlineKeyboardMarkup(row_width=2)

btn_cancel_agent = InlineKeyboardButton(text='Не будет сотрудничать 🚫', callback_data=example_data.new(move='cancel_agent'))
btn_jira = InlineKeyboardButton(text='Заявка в JIRA 📫', callback_data=example_data.new(move='jira'))

kb_div_inline.row(btn_cancel_agent, btn_jira)