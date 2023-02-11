from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.standart.main_menu import change_digit
from keyboards import kb_digit

@dp.message_handler()
async def mes_all(message: Message):
    if message.text.isdigit():
        change_digit()
        await message.answer(f'{message.from_user.first_name} Гляди! Цифра! - {message.text}', reply_markup=kb_digit)
    else:
        await message.answer(f'{message.from_user.first_name} Гляди! Буква! - {message.text}',
                             reply_markup=ReplyKeyboardRemove())
