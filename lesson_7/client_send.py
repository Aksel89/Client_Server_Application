import argparse
import socket
import time
import json
import sys
import os


sys.path.append(os.path.join(os.getcwd(), '..'))
import log.config_client_log

from decors import log
from logging import getLogger
from common.utils import get_message, send_message
from common.variables import *
from errors import *

LOGGER = getLogger('client')


@log
def message_from_server(message):
    """
    Функция обрабатывает сообщения других пользователей
    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message \
            and MESSAGE_TEXT in message:
        print(f'Получено сообщение от {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOGGER.info(f'Получено сообщение от {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """
    Функция запрашивает и возвращает сообщение, при порлучении "exit" завершает работу
    """
    message = input('Введите сообщение или "exit" для завершения работы: ')
    if message == 'exit':
        sock.close()
        LOGGER.info('Завершение работы по команде пользователя.')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
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
        },
        'encoding': ENCODING,
    }
    LOGGER.info(f'Create message: {message} from user {account_name}')
    return message


@log
def process_ans(answer):
    """
    Функция разбирает ответ сервера
    :param answer:
    :return:
    """
    LOGGER.debug(f'Server response: {answer}')
    if RESPONSE in answer:
        if answer[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {answer[ERROR]}'
    raise ValueError


@log
def arg_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        LOGGER.critical(
            f'Attempt to launch a client with an incorrect port number: {server_port}. '
            f'Valid addresses are 1024 to 65535. The client is being terminated.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        LOGGER.critical(f'Invalid operation mode is specified {client_mode}, '
                        f'Acceptable modes: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    """
    Функция работы через командную строку.
    client.py -p < номер порта в диапазоне [1024-65535} > -a < IP адрес клиента >
    Если нет параметров - используются параметры, заданные по-умолчанию
    :return:
    """
    server_address, server_port, client_mode = arg_parser()

    LOGGER.info(
        f'The client with the parameters is running: server address - {server_address}, '
        f'port - {server_port}, operating mode - {client_mode}')

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        LOGGER.info(f'A connection to the server has been established. Server response: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        LOGGER.error('The received JSON string could not be decoded.')
        sys.exit(1)
    except ServerError as error:
        LOGGER.error(f'When establishing a connection, the server returned an error: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOGGER.error(f'The required field is missing in the server response {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER.critical(
            f'Failed to connect to the server {server_address}:{server_port}, '
            f'the destination computer rejected the connection request.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'The connection to the {server_address} server has been lost.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'The connection to the {server_address} server has been lost.')
                    sys.exit(1)


if __name__ == "__main__":
    main()
