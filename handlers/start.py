from loader import dp
from aiogram.types import Message
from keyboards import kb_menu

@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    user_id = message.from_user.id
    await message.answer(f'Привет, твой id {user_id}. '
                         f'Передай его администратору для дальнейшей работы с ботом', reply_markup=kb_menu)
