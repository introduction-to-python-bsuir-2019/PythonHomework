import csv

def csv_writer(path, fieldnames, data):
    """
    Функция для записи в файл csv
    path - путь до файла
    fieldnames - название столбцов
    data - список из списков
    """
    with open(path, "w", newline='') as out_file:
        '''
        out_file - выходные данные в виде объекта
        delimiter - разделитель :|;
        fieldnames - название полей (столбцов)
        '''
        writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# если точка входа наш скрипт
def test(articles):
    data = articles

    my_list = []
    fieldnames = data[0]
    cell = data[1:]
    print('столбцы', fieldnames)
    print('ячейки(строки)', cell)
    for values in cell:
        print('строки', values)
        inner_dict = dict(zip(fieldnames, values))
        my_list.append(inner_dict)

    path = "dict_output.csv"
    csv_writer(path, fieldnames, my_list)