from loader import db, dp
from keyboards import kb_div_inline


async def add_new_comment(data: dict):
    """
    Через add_dump_comm обновляет комментарий в БД агентов в работе. Формирует лист с id пользователей через
    get_user_access и циклом for перебирает их, отправляя сообщение с text_mess (формируется из agent_data от
    get_dump_agent, поиск по ИНН)
    :param data: {'inn_number': '(ИНН)', 'comment': 'сотрудничает с (название компании)'}
    :return: dp.bot.send_message
    """
    agent_data = db.get_dump_agent(inn_number=data.get('inn_number'))[0]
    if agent_data[7] != '':
        data['comment'] = agent_data[7] + ", " + data.get('comment')
    db.add_dump_comm(data)
    my_adminset = db.get_user_access(user_role='admin')
    my_divset = db.get_user_access(user_role='divisional_mentor')
    if my_divset:
        my_adminset.extend(my_divset)
    text_mess = f"ФИО: {agent_data[1]}\nТелефон: {agent_data[2]}\nИНН: {agent_data[3]}\n" \
                f"Компания: {agent_data[4]}\n{data.get('comment')}"
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=kb_div_inline)


def update_agent_comment(data: set, new_data: dict):
    """
    перезаписывает комментарий в БД агентов в работе
    :param data: (id, 'ФИО', телефон, ИНН, компания, время записи, № строки, комментарий)
    :param new_data: {'agent_name': ", 'phone_number': '', 'inn_number': '', 'role': '', 'company_name': ''}
    :return:
    """
    comment = data[7]
    if comment == "": new_comment = 'данные обновлены'
    else: new_comment = comment + ', ' + 'данные обновлены'
    writing_dict = {'agent_name': new_data.get('agent_name'), 'phone_number': new_data.get('phone_number'),
                    'inn_number': new_data.get('inn_number'), 'comment': new_comment,
                    'id': data[0]}
    db.update_dump_comm(writing_dict)


