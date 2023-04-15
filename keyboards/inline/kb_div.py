from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import application_jira

kb_div_inline = InlineKeyboardMarkup(row_width=2)

btn_cancel_agent = InlineKeyboardButton(text='Не будет сотрудничать 🚫',
                                        callback_data=application_jira.new(jira='cancel_agent'))
btn_jira = InlineKeyboardButton(text='Заявка в JIRA 📫', callback_data=application_jira.new(jira='jira'))

kb_div_inline.row(btn_cancel_agent, btn_jira)
