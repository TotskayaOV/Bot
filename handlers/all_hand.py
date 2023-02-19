from loader import dp
from aiogram.types import Message

@dp.message_handler()
async def mes_all(message: Message):
    if message.text.isdigit():
        await message.answer(f'{message.from_user.first_name} Гляди! Цифра! - {message.text}')
    else:
        await message.answer(f'{message.from_user.first_name} Гляди! Буква! - {message.text}')
