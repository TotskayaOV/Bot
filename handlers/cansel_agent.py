from loader import dp
from aiogram.types import CallbackQuery
from keyboards import cancel_agent_div, application_jira
from working import div_cancel_agent


# "text": "ФИО:Иванов Иван Иванович\nТелефон: 79163000079\nИНН:79199700600\nКомпания: Изилоджистик Мск"
@dp.callback_query_handler(cancel_agent_div.filter(cancel_agent='cancel_agent'))
async def cansel_div_agent(callback: CallbackQuery):
    string_callback = callback.message.text
    user_id = callback.from_user.id
    my_list = string_callback.split('\n')
    agent_dict = {'last_user': user_id}
    for i in range(len(my_list) - 1):
        agent_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    div_cancel_agent(agent_dict)

@dp.callback_query_handler(application_jira.filter(jira='cancel_agent'))
async def cansel_div_agent(callback: CallbackQuery):
    string_callback = callback.message.text
    user_id = callback.from_user.id
    my_list = string_callback.split('\n')
    agent_dict = {'last_user': user_id}
    for i in range(len(my_list) - 1):
        agent_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    div_cancel_agent(agent_dict)