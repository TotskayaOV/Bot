from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db

# admins = [1, 2]
# coordinators = [1, 2]
# divisional_mentors = [1, 2]


class AddUserRole(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        try:
            my_set = db.get_user_access(user_id=message.from_user.id)
            user_role = list(*my_set)[3]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
            if user_role == 'divisional_mentor':
                data['divisional_mentor'] = True
            else:
                data['divisional_mentor'] = False
        except:
            data['guest'] = True

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        try:
            my_set = db.get_user_access(user_id=call.message.chat.id)
            user_role = list(*my_set)[3]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
            if user_role == 'divisional_mentor':
                data['divisional_mentor'] = True
            else:
                data['divisional_mentor'] = False
        except:
            data['guest'] = True
