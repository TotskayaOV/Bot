# Формирует словарь с данными для карточки агента
def writing_data(num_agent: int, num_string: int, gsheet_value: dict):
    if num_agent == 1 or num_agent == 4 or num_agent == 5 or num_agent == 6:
        agent_list = gsheet_value.get('values')[num_string - 1]
        match num_agent:
            case 1: company_name = 'Изилоджистик Мск'
            case 4: company_name = 'Л Карго СПб'
            case 5: company_name = 'Изилоджистик СПб'
            case 6: company_name = 'Изилоджистик Казань'
        if len(agent_list) < 11:
            role = 'Универсал'
        else:
            role = agent_list[10]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number':  agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': company_name
        }
    elif num_agent == 2:
        agent_list = gsheet_value.get('values')[num_string - 1]
        if len(agent_list) < 8 or agent_list[7] == '':
            role = 'Универсал'
        else:
            role = agent_list[7]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[2],
            'inn_number':
            agent_list[4],
            'role': role,
            'company_name': 'Я го'
        }
    elif num_agent == 3:
        agent_list = gsheet_value.get('values')[num_string - 1]
        if len(agent_list) < 12:
            role = 'Универсал'
        else:
            role = agent_list[11]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[3],
            'inn_number': agent_list[5],
            'role': role,
            'company_name': 'Л Карго Мск'
        }
    return data


def rewriting_data(num_agent: int, num_string: int, gsheet_value: dict):
    if num_agent == 1 or num_agent == 4 or num_agent == 5 or num_agent == 6:
        agent_list = gsheet_value.get('values')[0]
        match num_agent:
            case 1: company_name = 'Изилоджистик Мск'
            case 4: company_name = 'Л Карго СПб'
            case 5: company_name = 'Изилоджистик СПб'
            case 6: company_name = 'Изилоджистик Казань'
        if len(agent_list) < 11:
            role = 'Универсал'
        else:
            role = agent_list[10]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number':  agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': company_name
        }
    elif num_agent == 2:
        agent_list = gsheet_value.get('values')[0]
        if len(agent_list) < 8 or agent_list[7] == '':
            role = 'Универсал'
        else:
            role = agent_list[7]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[2],
            'inn_number': agent_list[4],
            'role': role,
            'company_name': 'Я го'
        }
    elif num_agent == 3:
        agent_list = gsheet_value.get('values')[0]
        if len(agent_list) < 12:
            role = 'Универсал'
        else:
            role = agent_list[11]
        if len(agent_list) < 5:
            count_append = 5 - len(agent_list)
            while count_append <= 5:
                agent_list.append('')
                count_append += 1
        data = {
            'agent_name': agent_list[1],
            'phone_number': agent_list[3],
            'inn_number': agent_list[5],
            'role': role,
            'company_name': 'Л Карго Мск'
        }
    return data


def name_company_number(full_name_company: str):
    """
    Принимает название компании, возвращает ее номер
    :param full_name_company: название компании
    :return: номер компании
    """
    match full_name_company:
        case 'Изилоджистик Мск': num_table = 1
        case 'Я го': num_table = 2
        case 'Л Карго Мск': num_table = 3
        case 'Л Карго СПб': num_table = 4
        case 'Изилоджистик СПб': num_table = 5
        case 'Изилоджистик Казань': num_table = 6
    return num_table


def number_company_name(number_company: int):
    """
    Принимает номер компании, возвращает ее название
    :param number_company: номер компании
    :return: название компании (str)
    """
    match number_company:
        case 1: name_company = 'Изилоджистик Мск'
        case 2: name_company = 'Я го'
        case 3: name_company = 'Л Карго Мск'
        case 4: name_company = 'Л Карго СПб'
        case 5: name_company = 'Изилоджистик СПб'
        case 6: name_company = 'Изилоджистик Казань'
    return name_company
