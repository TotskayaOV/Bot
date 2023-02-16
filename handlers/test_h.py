from loader import dp
from aiogram.types import Message
from external_database import GoogleTable

@dp.message_handler(commands=['test'])
async def mes_test(message_from: Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    result = text_msg.lower().split(' ')
    command = result[0]
    number = ['Можно платить']
    # command, number = text_msg.lower().split(' ')
    print(f"Вход: команда '{command}', опция '{number}'")

    values: str = GoogleTable.search_agent_izimsk(number)
    if values == -1:
        message = f'Такого абонемента не существует, либо его срок действия закончился 😰'
    else:
        agent_name: str = str(values[0])
        phone_number: int = int(values[1])
        inn_number: int = int(values[2])
        role_agent: str = str(values[3])
        result_st: str = str(values[4])
        message: str = f'Статус {number} у {agent_name} {phone_number} {inn_number} {role_agent} {result_st}'
    await message_from.reply(message)