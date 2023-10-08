import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message
from keyboards import kb_cancel_fsm
from .see_wb import string_current_tasks
class DoneAgent(StatesGroup):
    task_id = State()


@dp.message_handler(commands=['del_ca'], state=None)
async def delete_task_ca(message: Message, admin: bool):
        if admin:
            await message.answer(text='Введите id задачи', reply_markup=kb_cancel_fsm)
            await DoneAgent.task_id.set()
        else:
            await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=DoneAgent.task_id)
async def task_id_catch(message: Message, state: FSMContext):
            await state.update_data({'task_id': message.text})
            data = await state.get_data()
            num_id = data.get('task_id')
            try:
                db.remove_table_com_applications(num_id)
                await message.answer(f"Задача с id {num_id} удалена")
            except sqlite3.OperationalError:
                await message.answer("Ошибка удаления записи! Проверьте правильность вводимых данных")
            await state.reset_data()
            await state.finish()
