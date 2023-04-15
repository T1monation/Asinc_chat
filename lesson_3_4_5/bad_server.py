from socket import *
import time
import json


def main():

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('localhost', 7777))
    server.listen(5)

    client, addr = server.accept()

    while True:
        data = client.recv(100000)
        client.send(json.dumps({'test': 1, 'bad': 0}).encode('utf-8'))


if __name__ == '__main__':
    main()
