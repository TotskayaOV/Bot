from loader import dp
from aiogram.types import CallbackQuery
from keyboards import application_jira
from working import div_jira_agent
from .cb_parsing import callback_parsing


@dp.callback_query_handler(application_jira.filter(jira='jira'))
async def jira_div_agent(callback: CallbackQuery):
    agent_dict = callback_parsing(callback.message.text, callback.from_user.id)
    div_jira_agent(agent_dict)
