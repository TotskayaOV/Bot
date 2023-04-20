import xlsxwriter
from loader import db
# открываем новый файл на запись
workbook = xlsxwriter.Workbook('hello.xlsx')
# создаем там "лист"
worksheet = workbook.add_worksheet()
# в ячейку A1 пишем текст
worksheet.write('A1', 'Hello world')
# сохраняем и закрываем
workbook.close()
worksheet.write(0, 0, 'Это A1!')
worksheet.write(4, 3, 'Колонка D, стока 5')

def uploading_file(data):
    workbook = xlsxwriter.Workbook('temp_dir/pivot.xlsx')
    worksheet = workbook.add_worksheet()
    #id INTEGER PRIMARY KEY AUTOINCREMENT,
        # agent_name TEXT, phone_number INTEGER, inn_number INTEGER,
        # company_name TEXT, date_up DATETIME, date_down DATETIME, comment TEXT, last_user INTEGER
    for i in range(len(data)):
        for y in range(len(data[i])):
            worksheet.write(i, y, data[i][y])
    workbook.close()