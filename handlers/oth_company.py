from loader import dp
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from keyboards import example_data
from keyboards import kb_cancel_fsm
from working import add_new_comment
class OtherCompany(StatesGroup):
    inn_number = State()
    comment = State()

# "text": "ФИО:Иванов Иван Иванович\nТелефон: 79163000079\nИНН:79199700600\nКомпания: Изилоджистик Мск"
@dp.callback_query_handler(example_data.filter(move='banan'), state=None)
async def inn_agent(callback: CallbackQuery, state: FSMContext, message=None):
    await OtherCompany.inn_number.set()
    message = callback.message
    string_callback = callback.message.text
    my_list = string_callback.split('\n')
    agent_dict = {}
    for i in range(len(my_list)):
        agent_dict[my_list[i].split(':')[0]] = my_list[i].split(':')[1]
    await state.update_data({'inn_number': agent_dict.get('ИНН')})
    await message.answer(text='Напишите название компании, в которой оказывает услуги агент',
                         reply_markup=kb_cancel_fsm)
    await OtherCompany.next()

@dp.message_handler(state=OtherCompany.comment)
async def company_catch(message: Message, state: FSMContext):
    await state.update_data({'comment': f'сотрудничает с {message.text}'})
    data = await state.get_data()
    print(data)
    await add_new_comment(data)
    await state.reset_data()
    await state.finish()
