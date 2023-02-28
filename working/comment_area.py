from loader import db, dp
from working import chat_text
from datetime import datetime
from external_database import writing_status
from send_massage import notify

# {'inn_number': '771984557890', 'comment': 'сотрудничает с cheburator'}
async def add_new_comment(data: dict):
    db.add_dump_comm(data)
    my_adminset = db.get_user_access(user_role='admin')
    my_divset = db.get_user_access(user_role='divisional_mentor')
    my_adminset.extend(my_divset)
    agent_data = db.get_dump_agent(inn_number=data.get('inn_number'))
    print(agent_data)
    text_mess = f"ФИО: {agent_data[0][1]}\nТелефон: {agent_data[0][2]}\nИНН: {agent_data[0][3]}\n" \
                f"Компания: {agent_data[0][4]}\n{agent_data[0][7]}"
    for y in range(len(my_adminset)):
        chat_id = my_adminset[y][1]
        await dp.bot.send_message(chat_id, text=text_mess, reply_markup=None)
        print('done')