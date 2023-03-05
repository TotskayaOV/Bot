def column_comparison(table_dict: dict) -> list[int]:
    numbers_list = []
    for i, item in enumerate(table_dict.get('values')):
        if 'Может работать' in item and not ('Активирован') in item and i != 0:
            if 'Может работать' in item and ('Не хватает данных') not in item:
                numbers_list.append(i + 1)
    return (numbers_list)
