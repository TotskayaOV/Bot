from loader import dp
from aiogram.types import CallbackQuery
from keyboards import other_company
from working import add_new_comment


# "text": "ФИО:Иванов Иван Иванович\nТелефон: 79163000079\nИНН:79199700600\nКомпания: Изилоджистик Мск"
@dp.callback_query_handler(other_company.filter(verif='error_inn_data'))
async def error_phone_agent(callback: CallbackQuery, message=None):
    print("Done")
    message = callback.message
    string_callback = callback.message.text
    my_list = string_callback.split('\n')
    temp_dict = {}
    for i in range(len(my_list)):
        temp_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    data = {}
    data['inn_number'] = temp_dict.get('ИНН')
    data['comment'] = 'ошибка в номере ИНН'
    print(data)
    await add_new_comment(data)

@dp.callback_query_handler(other_company.filter(verif='error_phone_data'))
async def error_inn_agent(callback: CallbackQuery, message=None):
    print("Done")
    message = callback.message
    string_callback = callback.message.text
    my_list = string_callback.split('\n')
    temp_dict = {}
    for i in range(len(my_list)):
        temp_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    data = {}
    data['inn_number'] = temp_dict.get('ИНН')
    data['comment'] = 'ошибка в номере телефона'
    print(data)
    await add_new_comment(data)