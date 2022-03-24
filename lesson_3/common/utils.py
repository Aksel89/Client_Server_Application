import json
from variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(client):
    """
    Функция принимает и декодирует сообщения. Сообщение принимает в байтах --> выдает словарь.
    При приеме любого другого типа данных возвращает ошибку значения.
    :param client:
    :return:
    """
    encoding_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoding_response, bytes):
        json_response = encoding_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    """
    Функция кодирует и отправляет сообщение.
    Принимает словарь и отправляет его.
    :param sock:
    :param message:
    :return:
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
