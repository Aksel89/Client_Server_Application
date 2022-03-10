from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import json
from common.variables import *
from common.utils import get_message, send_message


def process_client_message(message):
    """
    Функция принимает и обрабатывает сообщения от клиента в виде словаря.
    Проверяет корректность и возвращает ответ для клиента в виде словаря.
    :param message:
    :return:
    """
    if ACTION in message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSE: 400,
        ERROR: 'BAD REQUEST'
    }


def main():
    """
    Функция работы через командную строку.
    client.py -p < номер порта в диапазоне [1024-65535} > -a < IP адрес - слушает сервер >
    Если нет параметров - используются параметры, заданные по-умолчанию
    :return:
    """
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print("После параметра '-р' необходимо указать номер порта")
        sys.exit(1)
    except ValueError:
        print('Порт можно указывать только в диапазоне от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print("После параметра '-а' необходимо указать  IP адрес, который будет слушать сервер")
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_addr = transport.accept()  # Принимаем запрос на соединение
        try:
            print('Получен запрос на соединение от %s' % str(client_addr))
            message_to_client = get_message(client)
            print(message_to_client)
            response = process_client_message(message_to_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорректное сообщение')
            client.close()


if __name__ == "__main__":
    main()
