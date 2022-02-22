"""
Конфигурационный файл с необходимыми переменными
"""
# Порт по умолчанию

DEFAULT_PORT = 7777
# IP адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальное количество подключений
MAX_CONNECTIONS = 5
# Максимальная длина сообщения (байт)
MAX_PACKAGE_LENGTH = 1024
# Кодировка
ENCODING = 'utf-8'


# Ключи для JIM протокола
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'ACCOUNT_NAME'


# Служебные ключи подключений
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONDEFAULT_IP_ADDRESSE = 'respondefault_ip_addresse'
BAD_REQUEST = 'BAD_REQUEST'
