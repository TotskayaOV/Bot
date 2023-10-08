from loader import dp
from aiogram.types import CallbackQuery
from keyboards import other_company
from working import add_new_comment
from .cb_parsing import callback_parsing


@dp.callback_query_handler(other_company.filter(verif='error_inn_data'))
async def error_phone_agent(callback: CallbackQuery):
    temp_dict = callback_parsing(callback.message.text, callback.from_user.id)
    data_err_inn = {'phone_number': temp_dict.get('Телефон'), 'comment': 'ошибка в номере ИНН'}
    await add_new_comment(data_err_inn, temp_dict.get('last_user'))


@dp.callback_query_handler(other_company.filter(verif='error_phone_data'))
async def error_inn_agent(callback: CallbackQuery):
    temp_dict = callback_parsing(callback.message.text, callback.from_user.id)
    data_err_phone = {'inn_number': temp_dict.get('ИНН'), 'comment': 'ошибка в номере телефона'}
    await add_new_comment(data_err_phone, temp_dict.get('last_user'))
