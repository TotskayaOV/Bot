import xlsxwriter
import datetime


def uploading_file(data, data2):
    workbook = xlsxwriter.Workbook('pivot.xlsx')
    worksheet = workbook.add_worksheet('Task')
    for i in range(len(data)):
        for y in range(len(data[i])):
            worksheet.write(i, y, data[i][y])
    if data2:
        worksheet2 = workbook.add_worksheet('Comment')
        for i in range(len(data2)):
            for y in range(len(data2[i])):
                worksheet2.write(i, y, data2[i][y])
    workbook.close()

def uploading_file_period(data, data2, dict_data: dict):
    workbook = xlsxwriter.Workbook('pivot.xlsx')
    worksheet = workbook.add_worksheet('Task')
    date1 = datetime.datetime.strptime(dict_data.get('up_date'), '%d-%m-%Y')
    date2 = datetime.datetime.strptime(dict_data.get('to_date'), '%d-%m-%Y')
    num_str = 1
    num_str2 = 1
    for i in range(len(data)):
        date_record = data[i][5].split(' ')[0]
        if datetime.datetime.strptime(date_record, '%d-%m-%Y') >= date1 \
                and datetime.datetime.strptime(date_record, '%d-%m-%Y') <= date2:
            for y in range(len(data[i])):
                worksheet.write(num_str, y, data[i][y])
            num_str +=1
    if data2:
        worksheet2 = workbook.add_worksheet('Comment')
        for i in range(len(data2)):
            date_record = data2[i][6].split(' ')[0]
            if datetime.datetime.strptime(date_record, '%d-%m-%Y') >= date1 \
                    and datetime.datetime.strptime(date_record, '%d-%m-%Y') <= date2:
                for y in range(len(data2[i])):
                    worksheet2.write(num_str2, y, data2[i][y])
                num_str2 += 1
    workbook.close()
