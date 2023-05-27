import select
from socket import *
from time import sleep


address = ('localhost', 10000)


def client_send():
    print('start client-send')
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        for el in range(3):
            msg = "test message"
            sock.send(msg.encode('utf-8'))
            sleep(1)
    exit(0)


if __name__ == '__main__':
    client_send()
