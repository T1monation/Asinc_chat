# Задание 1.
import re
import csv
from chardet.universaldetector import UniversalDetector


def encode_detect(file: str):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
            detector.close()
    return detector.result


# Слегка отходим от задания: делаем общий список, в котором будет сводная
# таблица по всем прочитанным файлам
def get_data(file_list: list):
    file_name = []
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data_list = []
    main_data_list.append(
        ['Имя файла', 'Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'])
    os_prod_pattern = r'\Bвитель системы:'
    os_name_pattern = r'\Bвание \D{2}:'
    os_code_pattern = r'\Bд продукта:'
    os_type_pattern = r'\Bп системы:'
    for el in file_list:
        encoding = encode_detect(el)
        with open(el, 'r', encoding=encoding['encoding']) as f:
            file_name.append(el)
            for row in f:
                match_prod = re.search(os_prod_pattern, row)
                if match_prod:
                    os_prod_list.append(re.split(r':', row)[1].strip())
                match_name = re.search(os_name_pattern, row)
                if match_name:
                    os_name_list.append(re.split(r':', row)[1].strip())
                match_code = re.search(os_code_pattern, row)
                if match_code:
                    os_code_list.append(re.split(r':', row)[1].strip())
                match_type = re.search(os_type_pattern, row)
                if match_type:
                    os_type_list.append(re.split(r':', row)[1].strip())

    temp_list = list(map(lambda x, y, z, q, w: [x, y, z, q, w],
                         file_name, os_prod_list, os_name_list, os_code_list, os_type_list))
    main_data_list.extend(temp_list)
    return main_data_list


def write_to_csv(file: str, files: list):
    data = get_data(files)
    with open(file, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        for row in data:
            f_writer.writerow(row)


if __name__ == '__main__':
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    print(get_data(files))
    write_to_csv('output.csv', files)
