import xlsxwriter


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