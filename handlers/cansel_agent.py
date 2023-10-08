from loader import dp
from aiogram.types import CallbackQuery
from keyboards import cancel_agent_div, application_jira
from working import div_cancel_agent
from .cb_parsing import callback_parsing


@dp.callback_query_handler(cancel_agent_div.filter(cancel_agent='cancel_agent'))
async def cansel_div_agent(callback: CallbackQuery):
    agent_dict = callback_parsing(callback.message.text, callback.from_user.id)
    div_cancel_agent(agent_dict)


@dp.callback_query_handler(application_jira.filter(jira='cancel_agent'))
async def cansel_div_agent(callback: CallbackQuery):
    agent_dict = callback_parsing(callback.message.text, callback.from_user.id)
    div_cancel_agent(agent_dict)
