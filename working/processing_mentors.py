from loader import db


def show_list_tags(company_name: str):
    """
    формирует лист тэгов для отправки сообщений в группу с наставниками
    :param company_name: скоращенное название компании (str)
    :return: строка тегов с @
    """
    mentors_list = db.get_all_mentors()
    match company_name:
        case 'Изилоджистик Мск' | 'Л Карго Мск' | 'Я го': city = 'Москва'
        case 'Л Карго СПб' | 'Изилоджистик СПб' : city = 'Санкт-Петербург'
        case 'Изилоджистик Казань': city = 'Казань'
    string_tags = ''
    for i in range(len(mentors_list)):
        if city in mentors_list[i]:
            string_tags += '@' + mentors_list[i][3] + ' '
    return string_tags
