from loader import dp
from aiogram.types import CallbackQuery
from keyboards import cancel_agent_div
from working import div_update_agent
from .cb_parsing import callback_parsing


# "text": "ФИО:Иванов Иван Иванович\nТелефон: 79163000079\nИНН:79199700600\nКомпания: Изилоджистик Мск"
@dp.callback_query_handler(cancel_agent_div.filter(cancel_agent='agent_update'))
async def update_div_agent(callback: CallbackQuery):
    agent_dict = callback_parsing(callback.message.text, callback.from_user.id)
    await div_update_agent(agent_dict)
