import time
import json
import sys
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import *


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии  клиента
    :param account_name:
    :return:
    """
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return message


def process_ans(answer):
    """
    Функция разбирает ответ сервера
    :param answer:
    :return:
    """
    if RESPONSE in answer:
        if answer[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {answer[ERROR]}'
    raise ValueError


def main():
    """
    Функция работы через командную строку.
    client.py -p < номер порта в диапазоне [1024-65535} > -a < IP адрес клиента >
    Если нет параметров - используются параметры, заданные по-умолчанию
    :return:
    """
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Порт можно указывать только в диапазоне от 1024 до 65535')
        sys.exit(1)

    client = socket(AF_INET, SOCK_STREAM)  # Сокет TCP
    client.connect((server_address, server_port))  # Соединение с сервером
    message_to_server = create_presence()
    send_message(client, message_to_server)
    try:
        answer = process_ans(get_message(client))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения')


if __name__ == "__main__":
    main()
