import select
from socket import *


address = ('localhost', 10000)


def client():
    app_mode = input(
        'Выберите режим работы клиента:\n[s] - "отправитель" сообщений\n'
        '[r] - "приемник" сообщений\n'
        'Введите режим: ')
    if app_mode not in ['r', 's']:
        print('Введен неправильный режим работы, клиент будет закрыт')
        exit(0)
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            if app_mode == 's':
                msg = input('Сообщение серверу: ')
                if msg == 'exit':
                    break
                sock.send(msg.encode('utf-8'))
            if app_mode == 'r':
                data = sock.recv(1024).decode('utf-8')
                print('Ответ: ', data)


if __name__ == '__main__':
    client()
