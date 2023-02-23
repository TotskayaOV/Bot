import os
from send_massage.send_messages import TelegramClient
# from external_database import column_comparison, values_Lk,values_Yg,values_IM



def notify(chat_id: int, text: str):
    telegram_client = TelegramClient(token=os.getenv('TOKEN'),
                                 base_url='https://api.telegram.org')
    my_params = {"chat_id": chat_id, "text": text}
    telegram_client.post(method='sendMessage', params=my_params)

