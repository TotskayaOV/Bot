from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .kb_cancel_fsm import btn_cancel


kb_role_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_admin = KeyboardButton(text='admin')
btn_coor = KeyboardButton(text='coordinator')
btn_divmen = KeyboardButton(text='divisional_mentor')

kb_role_user.add(btn_admin, btn_coor, btn_divmen)
kb_role_user.add(btn_cancel)



# kb_role_user = InlineKeyboardMarkup(row_width=3)
#
# btn_admin = InlineKeyboardButton(text='администратор', callback_data=role_callbk.new(user_role='admin'))
# btn_coor = InlineKeyboardButton(text='координатор', callback_data=role_callbk.new(user_role='coordinator'))
# btn_dm = InlineKeyboardButton(text='дивизионный наставник', callback_data=role_callbk.new(user_role='divisional_mentor'))
#
# kb_role_user.row(btn_admin).row(btn_coor).row(btn_dm)