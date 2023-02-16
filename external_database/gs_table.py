import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Подключение API:

CREDENTIALS_FILE = '../cbt.json'
spreadsheet_id1 = '1ammlfHCNNYwT7TEMyilZxcAEsDUgA4VWcGfjAnEhL2g'    #ИзиМск
spreadsheet_id2 = '12CVgah0l3YuD7s5P_hj6NyWZxO45GlN0XlWuRbvxo_E'    #Яго

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth =credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Чтение из таблицы (IM - ИзиМСК, Yg - Яго):
values_IM = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id1,
    range='A1:J4',
    majorDimension='COLUMNS'
).execute()
values_Yg = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id2,
    range='A1:J4',
    majorDimension='COLUMNS'
).execute()
print(values_IM)
print(values_Yg)

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