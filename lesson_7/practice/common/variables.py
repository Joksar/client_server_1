"""Константы"""
import logging
# Порт по умолчанию
DEFAULT_PORT = 6666
# IP по умолчанию
DEFAULT_IP_ADRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 10
# Максимальная длина сообщений в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
MESSAGE = 'message'
ERROR = 'error'
RESPONDEFAULT_IP_ADRESS = 'respondefault_ip_adress'
LOGGING_LEVEL = logging.DEBUG
MESSAGE_TEXT = 'mess_text'