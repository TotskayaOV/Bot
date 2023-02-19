import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Подключение API:

CREDENTIALS_FILE = 'cbt.json'
spreadsheet_id1 = '1ammlfHCNNYwT7TEMyilZxcAEsDUgA4VWcGfjAnEhL2g'    #ИзиМск - 1
spreadsheet_id2 = '12CVgah0l3YuD7s5P_hj6NyWZxO45GlN0XlWuRbvxo_E'    #Яго - 2
spreadsheet_id3 = '1qCzJA60FJnf0BN0vFnkgIazCejhLW-k8wg3BUSaLZek'    #Л-Карго -3

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth =credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Чтение из таблицы (IM - ИзиМСК, Yg - Яго):
values_IM = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id1,
    range='A1:K5',
    majorDimension='ROWS'
).execute()
values_Yg = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id2,
    range='A1:J',
    majorDimension='ROWS'
).execute()
values_Lk = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id3,
    range='A1:L',
    majorDimension='ROWS'
).execute()
print(values_IM)
print(values_Yg)
print(values_Lk)

def writing_status(row_num: str):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id2,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": row_num,
                 "majorDimension": "ROWS",
                 "values": [["Активирован"]]}
            ]
        }
    ).execute()
    print('Done')

def status_change(index_num: int, speedsheet_id: str):
    index_num = 5
    row_num = "J" + str(index_num)
    writing_status(row_num)
    worksheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id1,
        range='D:D',
        majorDimension='COLUMNS'
    ).execute()
# cell_list = worksheet.findall("Может работать")
    print(worksheet)

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