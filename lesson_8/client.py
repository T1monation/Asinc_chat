from multiprocessing import Process, JoinableQueue
from socket import *
import json
import time


def client_send(socket, q):
    while True:
        msg = q.get()
        socket.send(json.dumps(msg).encode('utf-8'))
        q.task_done()


def client_read(socket):
    while True:
        data = socket.recv(1024).decode('utf-8')
        if data:
            msg = json.loads(data)
            print(f'\n{msg["name"]}: {msg["msg"]}')


if __name__ == '__main__':
    address = ('localhost', 10000)
    name = input('Введите ваше имя: ')
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        q_send = JoinableQueue()
        cli_s = Process(target=client_send, args=(sock, q_send, ))
        cli_r = Process(target=client_read, args=(sock, ))
        cli_s.start()
        cli_r.start()
        while True:
            text = input('\n')
            q_send.put({'name': name, 'msg': text, 'action': 'msg',
                        'time': time.time(), })
