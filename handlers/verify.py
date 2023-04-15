from loader import dp
from aiogram.types import CallbackQuery
from keyboards import other_company
from working import verification_agent
from .cb_parsing import callback_parsing


@dp.callback_query_handler(other_company.filter(verif='verif'))
async def verif_agent(callback: CallbackQuery):
    agent_dict = callback_parsing(callback.message.text, callback.from_user.id)
    verification_agent(agent_dict)
