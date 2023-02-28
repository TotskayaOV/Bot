# Формирует словарь с данными для карточки агента
def writing_data(num_agent: int, num_string: int, gsheet_value: dict):
    if num_agent == 1:
        agent_list = gsheet_value.get('values')[num_string - 1]
        role = ''
        if len(agent_list) < 11:
            role = 'Универсал'
        else:
            role = agent_list[10]
        data = {
            'agent_name': agent_list[1],
            'phone_number':  agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': 'Изилоджистик Мск'
        }
    elif num_agent == 2:
        agent_list = gsheet_value.get('values')[num_string - 1]
        role = ''
        if agent_list[7] == '':
            role = 'Универсал'
        else:
            role = agent_list[7]
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': 'Я го'
        }
    elif num_agent == 3:
        agent_list = gsheet_value.get('values')[num_string - 1]
        role = ''
        if len(agent_list) < 12:
            role = 'Универсал'
        else:
            role = agent_list[11]
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[3],
            'inn_number': agent_list[5],
            'role': role,
            'company_name': 'Л Карго Мск'
        }
    return data