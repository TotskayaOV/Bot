from loader import db, dp
from datetime import datetime
from external_database import writing_status
from send_massage import notify



def call_admin(text_mess: str):
    my_adminset = db.get_user_access(user_role='admin')
    for i in range(len(my_adminset)):
        notify(my_adminset[i][1], text_mess)

# (44, 'Аннжелина Джоли', 79333064959, 972734238895, 'Л Карго Мск', '2023-02-26 22:51:31.480262', 3, '')
def sent_to_com_applications(agent_set: set):
    data_dict = {'agent_name': agent_set[1], 'phone_number': agent_set[2], 'inn_number': agent_set[3],
                 'company_name': agent_set[4], 'date_up': agent_set[5], 'date_down': datetime.now(),
                 'comment': agent_set[7]}
    return data_dict


# Получаем на вход данные типа dict: {'ФИО': 'Аннжелина Джоли', 'Телефон': ' 79333064959', 'ИНН': '972734238895', 'Компания': ' Л Карго Мск'}
# Из кортежа получаем id в dump (для последующего удаления), через функцию sent_to_com_applications формируем словарь
# для отправки в com_applications, получаем номер строки в которой нужно будет изменить статус
def verification_agent(data: dict):
    info_from_dump = db.get_dump_agent(inn_number=data.get('ИНН'))[0]
    text_mes = data.get('ФИО') + " " + data.get('Компания') + '\nверифицирован 🍌'
    call_admin(text_mes)
    id_agent_dump = info_from_dump[0]
    text_wdb = sent_to_com_applications(info_from_dump)
    num_row = info_from_dump[6]
    db.add_com_applications(text_wdb)
    db.remove_dump_agent(id_agent_dump)
    match text_wdb.get('company_name'):
        case 'Изилоджистик Мск': num_table = 1
        case 'Я го': num_table = 2
        case 'Л Карго Мск': num_table = 3
    writing_status(str(num_row), num_table)
