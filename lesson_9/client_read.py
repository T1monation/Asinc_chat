import select
from socket import *


address = ('localhost', 10000)


def client():
    print('start client-read')
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            data = sock.recv(1024).decode('utf-8')
            print('Ответ: ', data)


if __name__ == '__main__':
    client()
