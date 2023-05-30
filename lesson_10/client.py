from multiprocessing import Process, JoinableQueue
from socket import *
import json
import time
from metaclass import PortChecker, ClassVerifier


class Client(metaclass=ClassVerifier):
    port = PortChecker()

    def __init__(self, client_name='username', ip_addr='localhost', port=7777,):
        self.ip_addr = ip_addr
        self.port = port
        self.client_name = client_name

    def make_connection(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip_addr, self.port))

    @property
    def close_connection(self):
        self.cli_r.kill()
        self.cli_s.kill()
        self.socket.close()
        exit(0)

    @staticmethod
    def client_send_m(socket, q):
        while True:
            msg = q.get()
            socket.send(json.dumps(msg).encode('utf-8'))
            q.task_done()

    @staticmethod
    def client_read(socket):
        while True:
            data = socket.recv(1024).decode('utf-8')
            if data:
                msg = json.loads(data)
                print(f'\n{msg["name"]}: {msg["msg"]}')

    @property
    def start_message(self):
        self.queue_send = JoinableQueue()

        self.cli_s = Process(target=Client.client_send_m,
                             args=(self.socket, self.queue_send, ))
        self.cli_r = Process(target=Client.client_read,
                             args=(self.socket, ))
        self.cli_s.start()
        self.cli_r.start()
        print('Lets start chat:')
        while True:
            text = input('\n')
            if text == 'exit':
                self.close_connection
            self.queue_send.put({'name': self.client_name, 'msg': text, 'action': 'msg',
                                 'time': time.time(), })

    @property
    def start_chat(self):
        self.make_connection()
        self.start_message


if __name__ == '__main__':
    Client().start_chat
