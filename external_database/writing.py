from search import numbers_IM, numbers_Yg, numbers_Lk
from gs_table import values_IM, values_Yg, values_Lk

# Формирует словарь с данными для карточки агента
def writing_data(num_agent: int, num_string: int, gsheet_value: dict):
    if num_agent == 1:
        index_list = num_string - 1
        agent_list = gsheet_value.get('values')[index_list]
        role = ''
        if len(agent_list) < 11:
            role = 'Универсал'
        else:
            role = agent_list[10]
        data = {
            'agent_name': agent_list[1],
            'phone number':  agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': 'Изилоджистик'
        }
    elif num_agent == 2:
        index_list = num_string - 1
        agent_list = gsheet_value.get('values')[index_list]
        role = ''
        if agent_list[7] == '':
            role = 'Универсал'
        else:
            role = agent_list[7]
        data = {
            'agent_name': agent_list[1],
            'phone number': agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': 'Я го'
        }
    elif num_agent == 3:
        index_list = num_string - 1
        agent_list = gsheet_value.get('values')[index_list]
        role = ''
        if len(agent_list) < 12:
            role = 'Универсал'
        else:
            role = agent_list[11]
        data = {
            'agent_name': agent_list[1],
            'phone number': agent_list[3],
            'inn_number': agent_list[5],
            'role': role,
            'company_name': 'Л Карго'
        }
    return data

print(writing_data(2, numbers_Yg[0], values_Yg))
print(writing_data(1, numbers_IM[0], values_IM))
print(writing_data(3, numbers_Lk[0], values_Lk))