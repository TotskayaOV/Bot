from loader import dp
from aiogram.types import CallbackQuery
from keyboards import example_data
from working import div_update_agent


# "text": "ФИО:Иванов Иван Иванович\nТелефон: 79163000079\nИНН:79199700600\nКомпания: Изилоджистик Мск"
@dp.callback_query_handler(example_data.filter(move='agent_update'))
async def update_div_agent(callback: CallbackQuery):
    string_callback = callback.message.text
    my_list = string_callback.split('\n')
    agent_dict = {}
    for i in range(len(my_list) - 1):
        agent_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    await div_update_agent(agent_dict)
