from asyncio import sleep
from datetime import datetime, time

from aiogram.types import Message

from loader import dp, log_id
from working import cheking_workbase, call_admin, sent_admin_list
from send_massage import notify
from random import randint


@dp.message_handler(commands=['remove'])
async def mes_start(message: Message, admin: bool):
    if admin:
        restart = False
        sleep_time = 60
        hooligan_stickers = [r'CAACAgIAAxkBAAEI5b1kWJs1aR7MTkSRac0bjuYqkDd8ggAC0RYAAgk-4EsbCxDjDke45i8E',
                             r'CAACAgIAAxkBAAEI5b9kWJtJ6eRyrWPYi6TVNgeAN5x36QACTwUAAiMFDQABFxKC9MLEF2AvBA',
                             r'CAACAgIAAxkBAAEI5cFkWJteLy3l8Zbj_AIc9-_A1kJGBgACuiYAAoRPaEmv_Ezx_rhn-C8E',
                             r'CAACAgIAAxkBAAEI5cNkWJt14jZPZJOuVrVsAAFfx64TcBAAAmIUAAKMbOBLEYbNR4AKB7QvBA',
                             r'CAACAgIAAxkBAAEI5cVkWJu9PStTj7ome8XGc_Zg5EJAbAACegUAAiMFDQABbpLHbsuBRvUvBA',
                             r'CAACAgIAAxkBAAEI5cdkWJvb5TaOWQuMMdlaA8it8bJ3DQACmAUAAiMFDQABoc8KAXKxsyIvBA',
                             r'CAACAgIAAxkBAAEI5clkWJvxVFWdApSO67cvc9Pq14_dlAACjgUAAiMFDQAB_8ISUCLZ0Q0vBA',
                             r'CAACAgIAAxkBAAEI5c1kWJwd6NRZasL9LTuc08OqqkJvowACHxcAAldWYUqi1Bd7mXD-bS8E',
                             r'CAACAgIAAxkBAAEI5c9kWJxCcu7xzXyH4p-K_wqUl1AInwACQAQAAo-dWgUcdaCtPNiIlC8E',
                             r'CAACAgIAAxkBAAEI5dFkWJxOeNFxF72CJjCDZlmwvlOsfQACbAUAAo-dWgWXYQu0FK_CYS8E',
                             r'CAACAgIAAxkBAAEI5dNkWJyAtz-ELUYdVO6gKWwMYnM45QACOgQAAo-dWgUPoJfJo0airi8E',
                             r'CAACAgIAAxkBAAEI5dlkWJzFYmnkt1VPolY0DXKkJ8kYZQACwBEAAmcaoErrkdFHd0JoDC8E',
                             r'CAACAgIAAxkBAAEI5d1kWJ0fOn5DrDbgN0GZheHlmhQzPwAC4RMAAkM2CUuy6Zl4fQwPtS8E',
                             r'CAACAgIAAxkBAAEI5d9kWJ1AaDqloyn_rNNgjfqoiJ6N4AACuwoAAnOxeEsUTiJcG4o0mC8E',
                             r'CAACAgQAAxkBAAEI5edkWJ2fAhFPf2vRmUiQAuVGAQyMDgACSRgAAqbxcR7zOpD5Pmgbri8E',
                             r'CAACAgIAAxkBAAEI5etkWJ3n8ZAVEBC9pTkAAQMZW6GkVzgAAhkUAAIptdBJgyy8GPR_RBovBA',
                             r'CAACAgIAAxkBAAEI5e1kWJ32Owkq-EkmHFRB27dBhrXA3AACcBMAAgwPqEhaKHmNoUeobC8E',
                             r'CAACAgIAAxkBAAEI5fNkWJ4nvTezSrnYYWAWc2UGo7Cc4AACayEAAlaMCEqA92FgyPLptC8E]']
        while not restart:
            try:
                await cheking_workbase()
            except Exception as err:
                notify(log_id, f"{err}\n:: {datetime.now()} ::\nошибка подключения к Googlesheets\n{sleep_time}")
                if sleep_time == 25200:
                    sleep_time = 60
                else:
                    sleep_time += 30
            else:
                if sleep_time == 180:
                    call_admin('Всё окей 😉 Я пробился 😎 Работаем дальше 😇')
                    sleep_time = 60
                elif sleep_time == 25200:
                    random_index = randint(0, len(hooligan_stickers) - 1)
                    await sent_admin_list('Начинаем работать', hooligan_stickers[random_index])
                    sleep_time = 60
                else:
                    sleep_time = 60
            finally:
                if sleep_time == 180:
                    call_admin('‼️‼️‼️Ошибка подключения к Googlesheets 👿‼️‼️‼️')
                current_date_time = datetime.now()
                start_time = time(19, 0, 0)
                end_time = time(20, 0, 0)
                time_pause = current_date_time.time()
                if start_time <= time_pause <= end_time:
                    sleep_time = 25200
                await sleep(sleep_time)



