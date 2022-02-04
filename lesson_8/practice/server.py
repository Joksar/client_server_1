
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
    MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, \
    DESTINATION, EXIT
from common.utils import send_message, get_message
from decos import log

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, отправляет словарь-ответ в случае необходимости.
    :param message:
    :param messages_list:
    :param client:
    :param clients:
    :param names:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Вариант 1 - сообщение о присутствии + ответ
    if ACTION in message and message[ACTION] == PRESENCE \
            and TIME in message and USER in message:
        # Если такой пользователь еще не зарегистрирован,
        # регистрируем, иначе отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # Если это сообщение, то добавляем его в очередь сообщений.
    # Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # Иначе отдаем Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return

@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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

    # Словарь, содержащий имена пользователей и их сокеты.
    names = dict() #{client_name: client socket}

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

        # принимаем сообщения и если ошибка, исключаем клиента.
        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message, clients, names)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for i in messages:
            try:
                process_message(i, names, send_data_list)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряана.')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
    input('')
