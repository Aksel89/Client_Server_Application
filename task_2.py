"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""
word_1 = b'class'
word_2 = b'function'
word_3 = b'method'


def bytes_word(word):

    print(type(word), word, len(word))
    print('##########################')


if __name__ == "__main__":

    bytes_word(word_1)
    bytes_word(word_2)
    bytes_word(word_3)


