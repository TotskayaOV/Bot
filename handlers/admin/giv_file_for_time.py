import datetime
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db, log_id
from aiogram.types import Message, InputFile
from keyboards import kb_cancel_fsm
from send_massage import notify
from excel_worker import uploading_file_period


class UnloadingDate(StatesGroup):
    up_date = State()
    to_date = State()

# 21-04-2023 07:52:10

@dp.message_handler(commands=['unloading'], state=None)
async def unloading_for_period(message: Message, admin: bool):
    if admin:
        await message.answer(text='введите начало периода (в формате 01-01-2000)', reply_markup=kb_cancel_fsm)
        await UnloadingDate.up_date.set()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=UnloadingDate.up_date)
async def up_date_catch(message: Message, state: FSMContext):
    await state.update_data({'up_date': message.text})
    await message.answer(text='введите конец периода (в формате 01-01-2000)', reply_markup=kb_cancel_fsm)
    await UnloadingDate.next()


@dp.message_handler(state=UnloadingDate.to_date)
async def to_date_catch(message: Message, state: FSMContext):
    await state.update_data({'to_date': message.text})
    data = await state.get_data()
    try:
        date1 = datetime.datetime.strptime(data.get('up_date'), '%d-%m-%Y')
        date2 = datetime.datetime.strptime(data.get('to_date'), '%d-%m-%Y')
        if date2 >= date1:
            pass
        else:
            await message.answer(text='Вначале введите дату начала периода, второй - окончания\n'
                                      'Для получения выгрузки за период, начните сначала.')
    except Exception as err:
        await message.answer(text=f'Даты введены в некорректном формате или\n{err}')
    else:
        try:
            data_finally_task = db.get_all_com_applications()
            data_comment = db.get_all_comment_to_repository()
            uploading_file_period(data_finally_task, data_comment, data)
            path = 'pivot.xlsx'
            await message.answer_document(InputFile(path))
            os.remove(path)
        except Exception as err:
            await message.answer('Ошибка выгрузки из БД')
            notify(log_id, f"{err} :: ошибка выгрузки из БД")
    finally:
        await state.reset_data()
        await state.finish()
