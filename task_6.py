"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
 кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""
from chardet import detect

lines = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w', encoding='utf-8') as f_w:
    for line in lines:
        f_w.write(line + '\n')

with open('test_file.txt', 'rb') as f:
    content = f.read()

encoding = detect(content)['encoding']
print('encoding: ', encoding)

with open('test_file.txt', 'r', encoding=encoding) as f_r:
    for line in f_r:
        print(line, end='')
