
import sys
import select
import time
import argparse
import json
import logging
import logs.config_server_log
from errors import IncorrectDataReceivedError
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET,SO_REUSEADDR
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADRESS, \
    MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, ENCODING, \
    ACTION, TIME, USER, ACCOUNT_NAME, \
    PRESENCE, RESPONSE, ERROR, RESPONDEFAULT_IP_ADRESS, \
    MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import send_message, get_message
from decos import log

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Вариант 1 - сообщение о присутствии + ответ
    if ACTION in message and message[ACTION] == PRESENCE \
            and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Вариант 2 - обычное сообщение. Добавляется в очередь. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE \
            and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Вариант 3 - Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def create_arg_parser():
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # Проверка получения корректного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта'
                               f'{listen_port}. Допустимы значения с 1024 до 65535')
        sys.exit(1)

    return listen_address, listen_port

def main():
    """
    Загрузка парамтеров командной строки. Если параметров нет, то используется значение по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    """
    listen_address, listen_port = create_arg_parser()

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес, с которого принимаются подключения: {listen_address}, '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')


    # Готовим сокет
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # Список клиентов, очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    # Основной цикл сервера
    while True:
        # Ожидание подключения. Исключение по окончании времени.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        err_list = []
        # Проверка на наличие ждущих клиентов
        try:
            if clients:
                recv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если они есть, кладем в словарь,
        # если ошибка, исключаем клиента.
        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщения
        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                    print(f'Было отправлено сообщение: {message}')
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
