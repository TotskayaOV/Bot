import httplib2
import os
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Подключение API:

CREDENTIALS_FILE = './cred/cbt.json'
spreadsheet_id0 = os.getenv('SPSH0')    #Сводная
spreadsheet_id1 = os.getenv('SPSH1')    #ИзиМск - 1
spreadsheet_id2 = os.getenv('SPSH2')    #Яго - 2
spreadsheet_id3 = os.getenv('SPSH3')    #Л-Карго (Мск и СПБ) -3, 4
spreadsheet_id5 = os.getenv('SPSH5')    #ИзиСПб - 5
spreadsheet_id6 = os.getenv('SPSH6')    #ИзиКазань - 6

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


def google_search():
    values_IM = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id1,
        range='A1:K',
        majorDimension='ROWS'
    ).execute()
    values_Yg = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id2,
        range='A1:J',
        majorDimension='ROWS'
    ).execute()
    values_Lk = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id3,
        range="A1:L",
        majorDimension='ROWS'
    ).execute()
    values_LkSpb = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id3,
        # worksheets= 'Л Карго (СПБ)',
        range="'Л Карго (СПБ)'!A1:K",
        majorDimension='ROWS'
    ).execute()
    values_IS = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id5,
        range='A1:K',
        majorDimension='ROWS'
    ).execute()
    values_IK = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id6,
        range='A1:K',
        majorDimension='ROWS'
    ).execute()
    result_dict = {}
    result_dict['ИЗИ МСК'] = values_IM
    result_dict['ЯГО'] = values_Yg
    result_dict['Л КАРГО Мск'] = values_Lk
    result_dict['Л КАРГО Спб'] = values_LkSpb
    result_dict['ИЗИ СПб'] = values_IS
    result_dict['ИЗИ Казань'] = values_IK
    return result_dict


def google_update(row_num: str, comp_num: int):
    """
    match case определяет по номеру компании какой GooGlesheet ID использовать и в каком диапозоне производить поиск.
    переменная litera собирает нужный диапозон столбцов и номер строки в одну строку.
    :param row_num: номер строки
    :param comp_num: номер компании:
                        1. Изилоджистик Мск
                        2. Я го
                        3. Л Карго Мск
                        4. Л Карго СПб
                        5. Изилоджистик СПб
                        6. Изилоджистик Казань
    :return:
    """
    match comp_num:
        case 1:
            spreadsheetIdFunc = spreadsheet_id1
            litera = "A" + str(row_num) + ":" + "J" + str(row_num)
        case 2:
            spreadsheetIdFunc = spreadsheet_id2
            litera = "A" + str(row_num) + ":" + "J" + str(row_num)
        case 3:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "A" + str(row_num) + ":" + "K" + str(row_num)
        case 4:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "'Л Карго (СПБ)'!A" + str(row_num) + ":" + "K" + str(row_num)
        case 5:
            spreadsheetIdFunc = spreadsheet_id5
            litera = "A" + str(row_num) + ":" + "J" + str(row_num)
        case 6:
            spreadsheetIdFunc = spreadsheet_id6
            litera = "A" + str(row_num) + ":" + "J" + str(row_num)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetIdFunc,
        range=litera,
        majorDimension='ROWS'
    ).execute()
    return values


def writing_status(row_num: str, comp_num: int):
    match comp_num:
        case 1:
            spreadsheetIdFunc = spreadsheet_id1
            litera = "J"
        case 2:
            spreadsheetIdFunc = spreadsheet_id2
            litera = "J"
        case 3:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "K"
        case 4:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "'Л Карго (СПБ)'!J"
        case 5:
            spreadsheetIdFunc = spreadsheet_id5
            litera = "J"
        case 6:
            spreadsheetIdFunc = spreadsheet_id6
            litera = "J"
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetIdFunc,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": litera+row_num,
                 "majorDimension": "ROWS",
                 "values": [["Активирован"]]}
            ]
        }
    ).execute()

def writing_cancel_status(row_num: str, comp_num: int):
    match comp_num:
        case 1:
            spreadsheetIdFunc = spreadsheet_id1
            litera = "D"
        case 2:
            spreadsheetIdFunc = spreadsheet_id2
            litera = "D"
        case 3:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "E"
        case 4:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "'Л Карго (СПБ)'!D"
        case 5:
            spreadsheetIdFunc = spreadsheet_id5
            litera = "D"
        case 6:
            spreadsheetIdFunc = spreadsheet_id6
            litera = "D"
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetIdFunc,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": litera+row_num,
                 "majorDimension": "ROWS",
                 "values": [[""]]}
            ]
        }
    ).execute()


def writing_jira_status(row_num: str, comp_num: int):
    """
    Проставляет статус агенту в Googlesheet "Не хватает данных"
    :param row_num: номер строки (str)
    :param comp_num: номер таблицы (int)
    :return:
    """
    match comp_num:
        case 1:
            spreadsheetIdFunc = spreadsheet_id1
            litera = "J"+row_num
        case 2:
            spreadsheetIdFunc = spreadsheet_id2
            litera = "J"+row_num
        case 3:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "K"+row_num
        case 4:
            spreadsheetIdFunc = spreadsheet_id3
            litera = "'Л Карго (СПБ)'!J"+row_num
        case 5:
            spreadsheetIdFunc = spreadsheet_id5
            litera = "J"+row_num
        case 6:
            spreadsheetIdFunc = spreadsheet_id6
            litera = "J"+row_num
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetIdFunc,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": litera,
                 "majorDimension": "ROWS",
                 "values": [["Не хватает данных"]]}
            ]
        }
    ).execute()


def writing_pivot_table(all_data: tuple):
    """
    Данные приходят в виде списка кортежей
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT, phone_number INTEGER, inn_number INTEGER,
        company_name TEXT, date_up DATETIME, date_down DATETIME, comment TEXT, last_user INTEGER)'
    litera_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    :param all_data: данные из БД (tuple)
    :return:
    """
    spreadsheetIdFunc = spreadsheet_id0
    values_data = []
    for i in range(len(all_data)):
        values_data.append(list(all_data[i][1:]))
    range_data = "A2:H" + str(len(all_data)+1)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetIdFunc,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range_data,
                 "majorDimension": "ROWS",
                 "values": values_data}
            ]
        }
    ).execute()


# writing_status(3, '3')

# def status_change(index_num: int, speedsheet_id: str):
#     index_num = 5
#     row_num = "J" + str(index_num)
#     writing_status(row_num)
#     worksheet = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheet_id1,
#         range='D:D',
#         majorDimension='COLUMNS'
#     ).execute()
# # cell_list = worksheet.findall("Может работать")
#     print(worksheet)

# Запись в файл
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id1,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "B3:C4",
#              "majorDimension": "ROWS",
#              "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
#             {"range": "D5:E6",
#              "majorDimension": "COLUMNS",
#              "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
# 	]
#     }
# ).execute()
