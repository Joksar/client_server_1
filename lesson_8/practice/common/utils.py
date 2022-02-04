"""Утилиты"""
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
print(sys.path)
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
import json
from socket import socket, AF_INET, SOCK_STREAM
from decos import log

@log
def get_message(client):
    """
    Принимает сообщение, декодирует, конвертирует в словарь.
    :param client:
    :return:
    """

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError

@log
def send_message(sock, message):
    """Принимает словарь и отправляет его"""
    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)