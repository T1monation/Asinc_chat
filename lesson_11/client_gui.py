from multiprocessing import Process, JoinableQueue
from socket import *
import json
import time
from metaclass import PortChecker, ClassVerifier
import argparse
import logging
import sys
from PySide6.QtCore import SignalInstance, Signal, QObject


class Client(QObject):
    port = PortChecker()
    text = str()
    hashed_password = None

    def __init__(self, client_name='username', ip_addr='localhost', port=7777,):
        QObject.__init__(self)
        self.parsed_args = self.parser()
        self.queue_send = JoinableQueue()
        self.queue_read = JoinableQueue()
        self.new_message = Signal(dict)
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
    def client_send_m(socket, q: JoinableQueue):
        while True:
            msg = q.get()
            socket.send(json.dumps(msg).encode('utf-8'))
            q.task_done()

    @staticmethod
    def client_read(socket, q: JoinableQueue):
        while True:
            data = socket.recv(1024).decode('utf-8')
            if data:
                msg = json.loads(data)
                q.put(msg)

    @property
    def start_message(self):

        self.cli_s = Process(target=self.client_send_m,
                             args=(self.socket, self.queue_send, ))
        self.cli_r = Process(target=self.client_read,
                             args=(self.socket, self.queue_read,))
        self.cli_s.start()
        self.cli_r.start()
        self.log.info('Lets start chat!')

    @property
    def client_online_list(self):
        self.queue_send.put({'action': 'get_contacts', "name": self.client_name,
                            'time': time.time(), 'destination': 'self'})

    def client_to_del(self, name):
        self.queue_send.put({'name': self.client_name,
                             'action': 'del_contact',
                             'contact_to_del': name,
                             'time': time.time(),
                             'destination': 'self'})

    def client_to_add(self, name):
        self.queue_send.put(
            {'name': self.client_name,
             'action': 'add_contact',
             'contact_to_add': name,
             'time': time.time(),
             'destination': 'self'}
        )

    def register(self, login, password):
        self.queue_send.put(
            {
                "action": "register",
                "name": login,
                "password": password,
                "time": time.time(),
                "destination": "self"
            }
        )

    @property
    def presense(self):
        self.queue_send.put(
            {'name': self.client_name,
             'action': 'presense',
             'time': time.time(),
             'destination': 'self'}
        )

    def send_message(self, text: str):
        self.text = text
        if self.text.startswith('#e'):
            self.close_connection
        elif self.text.startswith('#cli'):
            self.queue_send.put({'name': self.client_name,
                                'msg': '', 'action': 'get_contacts',
                                 'time': time.time(),
                                 })
        elif self.text.startswith('#h'):
            print('Chat command: \n',
                  '#e - exit\n',
                  '#h - help\n',
                  '#cli - online clients list\n',
                  '#add:[frend_name] - add frend to contact',
                  '#del:[frend_name] - delete frend from contact',
                  '#fr - get frend list'
                  )
        elif self.text.startswith('#add'):
            frend_name = self.text.split('#add:')
            self.queue_send.put({'name': self.client_name,
                                'msg': '', 'action': 'add_contact',
                                 'contact_to_add': frend_name[1],
                                 'time': time.time(),
                                 'destination': 'self'})
        elif self.text.startswith('#del'):
            frend_name = self.text.split('#del:')
            self.queue_send.put({'name': self.client_name,
                                'msg': '', 'action': 'del_contact',
                                 'contact_to_del': frend_name[1],
                                 'time': time.time(),
                                 'destination': 'self'})
        elif self.text.startswith('#fr'):
            self.queue_send.put({'name': self.client_name,
                                'msg': '', 'action': 'get_frend_list',
                                 'time': time.time(),
                                 'destination': 'self'})
        else:
            self.queue_send.put({'name': self.client_name, 'msg': self.text, 'action': 'msg',
                                'time': time.time(), 'destination': 'other'})
        self.text = None

    @property
    def start_chat(self):
        self.make_connection()
        self.start_message


if __name__ == '__main__':
    Client().start_chat
