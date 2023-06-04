from multiprocessing import Process, JoinableQueue
from socket import *
import json
import time
from metaclass import PortChecker, ClassVerifier
import argparse
import logging
import sys


class Client(metaclass=ClassVerifier):
    port = PortChecker()

    def __init__(self, client_name='username', ip_addr='localhost', port=7777,):
        self.parsed_args = self.parser()
        if ip_addr != 'localhost':
            self.ip_addr = ip_addr
        else:
            self.ip_addr = self.parsed_args.addr
        if port != 7777:
            self.port = port
        else:
            self.port = self.parsed_args.port
        if client_name != 'username':
            self.port = client_name
        else:
            self.client_name = self.parsed_args.name
        self.log = logging.getLogger('server')
        self.log.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler(stream=sys.stdout)
        self.log.addHandler(self.handler)

    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(description="Server message app")
        parser.add_argument('--port', metavar='--p', type=int,
                            help='server TCP-port', default=7777)
        parser.add_argument('--addr', metavar='--a', type=str,
                            help='server address', default='localhost')
        parser.add_argument('--name', metavar='--n', type=str,
                            help='client name', default='username')
        return parser.parse_args()

    def make_connection(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip_addr, self.port))
        self.log.info(f'starting whith addres {self.ip_addr} port {self.port}')

    @property
    def close_connection(self):
        self.cli_r.kill()
        self.cli_s.kill()
        self.socket.close()
        self.log.info('Bye-bye, darling!')
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
        self.log.info('Lets start chat!')
        while True:
            text = input('\n')
            if text.startswith('#e'):
                self.close_connection
            elif text.startswith('#cli'):
                self.queue_send.put({'name': self.client_name,
                                     'msg': '', 'action': 'get_contacts',
                                     'time': time.time(), })
            elif text.startswith('#h'):
                print('Chat command: \n',
                      '#e - exit\n',
                      '#h - help\n',
                      '#cli - online clients list\n',
                      )
            else:
                self.queue_send.put({'name': self.client_name, 'msg': text, 'action': 'msg',
                                     'time': time.time(), })

    @property
    def start_chat(self):
        self.make_connection()
        self.start_message


if __name__ == '__main__':
    Client().start_chat
