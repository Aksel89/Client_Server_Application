import socket
import sys
import json
import argparse
import select
import time
import os
from common.variables import *
from common.utils import get_message, send_message
from logging import getLogger

sys.path.append(os.path.join(os.getcwd(), '..'))
import log.config_server_log

from decors import log

LOGGER = getLogger('server')


@log
def process_client_message(message):
    """
    Функция принимает и обрабатывает сообщения от клиента в виде словаря.
    Проверяет корректность и возвращает ответ для клиента в виде словаря.
    :param message:
    :return:
    """
    LOGGER.debug(f'Check message from client: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSE: 400,
        ERROR: 'BAD REQUEST'
    }


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOGGER.critical(
            f'Attempt to start the server with the wrong port '
            f'{listen_port}. Addresses from 1024 to 65535 are allowed.')
        sys.exit(1)

    return listen_address, listen_port


@log
def main():
    listen_address, listen_port = arg_parser()

    LOGGER.info(
        f'The server is running, the port for connections: {listen_port}, '
        f'the address from which connections are accepted: {listen_address}. '
        f'If the address is not specified, connections from any addresses are accepted.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)
    # Основной цикл программы сервера
    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)  # The error number returns None because it's just a timeout
            pass
        else:
            LOGGER.info(f'A connection has been established with {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER.info(f'Client {client_with_message.getpeername()} disconnected from the server.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Client {waiting_client.getpeername()} disconnected from the server.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == "__main__":
    main()
