import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db, admin_id
from aiogram.types import Message
from keyboards import kb_cancel_fsm, kb_choosing_city


# user_id INTEGER, name TEXT, user_tag TEXT, city TEXT
class NewMentor(StatesGroup):
    user_id = State()
    name = State()
    user_tag = State()
    city = State()


@dp.message_handler(commands=['mentor'], state=None)
async def add_mentor(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Введите id (только цифры)', reply_markup=kb_cancel_fsm)
        await NewMentor.user_id.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=NewMentor.user_id)
async def id_catch(message: Message, state: FSMContext):
    await state.update_data({'user_id': message.text})
    await message.answer(text='Введите Фамилию', reply_markup=kb_cancel_fsm)
    await NewMentor.next()


@dp.message_handler(state=NewMentor.name)
async def name_catch(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Укажите тэг пользователя (без @)', reply_markup=kb_cancel_fsm)
    await NewMentor.next()


@dp.message_handler(state=NewMentor.user_tag)
async def name_catch(message: Message, state: FSMContext):
    await state.update_data({'user_tag': message.text})
    await message.answer(text='Выберите в каком городе находится пользователь:', reply_markup=kb_choosing_city)
    await NewMentor.next()


@dp.message_handler(state=NewMentor.city)
async def name_catch(message: Message, state: FSMContext):
    if message.text in ['Москва', 'Казань', 'Санкт-Петербург']:
        await state.update_data({'city': message.text})
        data = await state.get_data()
        try:
            db.add_list_mentors(data)
            await message.answer(f"Пользователь {data.get('name')} из города {data.get('city')} успешно добавлен")
        except sqlite3.OperationalError:
            await message.answer("Ошибка добавления пользователя! Проверьте правильность вводимых данных")
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Выберите в каком городе находится пользователь:', reply_markup=kb_choosing_city)
