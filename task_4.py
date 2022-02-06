"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""


def word_encode_decode(word):

    print(type(word), word)

    print('####--Кодирование--#####')
    bytes_word = word.encode('utf-8')
    print(type(bytes_word), bytes_word)

    print('####--Декодирование--####')
    str_word = bytes_word.decode('utf-8')
    print(type(str_word), str_word)

    print('##########################')


if __name__ == "__main__":

    word_1 = 'разработка'
    word_2 = 'администрирование'
    word_3 = 'protocol'
    word_4 = 'standard'

    word_encode_decode(word_1)
    word_encode_decode(word_2)
    word_encode_decode(word_3)
    word_encode_decode(word_4)
