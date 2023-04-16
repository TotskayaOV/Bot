import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message
from keyboards import kb_cancel_fsm
from .see_wb import string_current_tasks
class DeleteAgent(StatesGroup):
    agent_id = State()


@dp.message_handler(commands=['del_dump'], state=None)
async def delete_user(message: Message, admin: bool):
        if admin:
            await message.answer(text=string_current_tasks())
            await message.answer(text='Введите id задачи', reply_markup=kb_cancel_fsm)
            await DeleteAgent.agent_id.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=DeleteAgent.agent_id)
async def id_user_catch(message: Message, state: FSMContext):
            await state.update_data({'agent_id': message.text})
            data = await state.get_data()
            agent_id = data.get('agent_id')
            try:
                db.remove_dump_agent(agent_id)
                await message.answer(f"Задача с id {agent_id} удалена")
            except sqlite3.OperationalError:
                await message.answer("Ошибка удаления пользователя! Проверьте правильность вводимых данных")
            await state.reset_data()
            await state.finish()
