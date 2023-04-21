import xlsxwriter


def uploading_file(data):
    workbook = xlsxwriter.Workbook('pivot.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(len(data)):
        for y in range(len(data[i])):
            worksheet.write(i, y, data[i][y])
    workbook.close()