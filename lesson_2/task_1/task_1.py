"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого: Создать
функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В
этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий
список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для
этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла); Создать функцию
write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов
функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл; Проверить работу программы
через вызов функции write_to_csv().
"""
import csv
import re
import chardet
import pathlib
from pathlib import Path


path_files = Path(pathlib.Path.cwd())


def get_data():

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    manufacturer = 'Изготовитель системы'
    os_name = 'Название ОС'
    product_code = 'Код продукта'
    type_of_system = 'Тип системы'


    #  iterate over files of a given range
    for i in range(1, 4):

        # open each file in byte representation, decode and read the necessary information using regexp
        with open(f'{path_files}/info_{i}.txt', 'rb') as f_obj:
            rawdata = f_obj.read()
            result = chardet.detect(rawdata)
            file = rawdata.decode(result['encoding'])

        # get the name of the manufacturer
        os_prod_get = re.compile(fr'{manufacturer}:\s*\S*')
        os_prod_list.append(os_prod_get.findall(file)[0].split()[2])

        # get the name OS
        os_name_reg = re.compile(r'Windows\s*\S*')
        os_name_list.append(os_name_reg.findall(file)[0])

        # get the product code
        os_code_reg = re.compile(fr'{product_code}:\s*\S*')
        os_code_list.append(os_code_reg.findall(file)[0].split()[2])

        # get the system type
        os_type_reg = re.compile(fr'{type_of_system}:\s*\S*')
        os_type_list.append(os_type_reg.findall(file)[0].split()[2])

    table_header = [manufacturer, os_name, product_code, type_of_system]
    main_data.append(table_header)

    received_data = [os_prod_list, os_name_list, os_code_list, os_type_list]

    for i in range(len(received_data[0])):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


def write_to_csv(out_file):

    main_data = get_data()
    with open(out_file, 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row in main_data:
           write.writerow(row)


write_to_csv('info.csv')

