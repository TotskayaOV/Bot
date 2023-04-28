import datetime
from loader import db, dp


def get_comments_db(data_tuple: tuple, last_user: int, comment: str):
    """
    на вход принимает данные агента из задач в раобте, id телеграмма проставившего комментарий и комментарий,
    для записи в таблицу данных комментариев
    :param data_tuple: (id, agent_name, phone_number, inn_number,company_name, date_up, row_number, comment)
    :param last_user: int id_user
    :param comment: str comment
    """
    dt_obj = datetime.datetime.now()
    data = {'agent_name': data_tuple[1], 'company_name': data_tuple[4], 'phone_number': data_tuple[2],
            'inn_number': data_tuple[3], 'comment': comment, 'date_up': dt_obj.strftime("%d-%m-%Y %H:%M:%S"),
            'user_id': last_user}
    db.add_comment_to_repository(data)


