from gs_table import values_IM, values_Yg, values_Lk

def column_comparison(table_dict: dict):
    numbers_list = []
    for i, item in enumerate(table_dict.get('values')):
        if 'Может работать' in item and not ('Активирован') in item and i != 0:
            if 'Может работать' in item and ('Не хватает данных') not in item:
                numbers_list.append(i + 1)
    return (numbers_list)

numbers_IM = column_comparison(values_IM)
numbers_Yg = column_comparison(values_Yg)
numbers_Lk = column_comparison(values_Lk)
print(f'пациент в строке {numbers_IM}')
print(f'пациент в строке {numbers_Yg}')
print(f'пациент в строке {numbers_Lk}')