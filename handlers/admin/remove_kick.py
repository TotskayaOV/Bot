import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message
from keyboards import kb_cancel_fsm
from .see_kick import string_kick_tasks
class KickTask(StatesGroup):
    task_id = State()


@dp.message_handler(commands=['del_kick'], state=None)
async def delete_task_kick(message: Message, admin: bool):
        if admin:
            await message.answer(text=string_kick_tasks())
            await message.answer(text='Введите id оповещения', reply_markup=kb_cancel_fsm)
            await KickTask.task_id.set()
        else:
            await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=KickTask.task_id)
async def task_id_catch(message: Message, state: FSMContext):
            await state.update_data({'task_id': message.text})
            data = await state.get_data()
            num_id = data.get('task_id')
            try:
                db.remove_task_kick(num_id)
                await message.answer(f"Оповещение с id {num_id} удалено")
            except sqlite3.OperationalError:
                await message.answer("Ошибка удаления записи! Проверьте правильность вводимых данных")
            await state.reset_data()
            await state.finish()