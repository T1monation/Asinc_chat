import select
from socket import *
from metaclass import ClassVerifier, PortChecker
import logging
import sys
import argparse


class Server(metaclass=ClassVerifier):
    clients = []
    port = PortChecker()
    socket = socket()

    def __init__(self, ip_addr='localhost', port=7777, max_clients=5, timeout=0.2):
        self.parsed_args = self.parser()
        if ip_addr != 'localhost':
            self.ip_addr = ip_addr
        else:
            self.ip_addr = self.parsed_args.addr
        if port != 7777:
            self.port = port
        else:
            self.port = self.parsed_args.port
        self.max_clients = max_clients
        self.timeout = timeout
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
        return parser.parse_args()

    def run_server(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.ip_addr, self.port))
        self.log.info(f'starting whith addres {self.ip_addr} port {self.port}')
        self.socket.listen(self.max_clients)
        self.socket.settimeout(self.timeout)

        while True:
            try:
                conn, addr = self.socket.accept()
                self.log.info(f'start connection on address: {addr}')
            except OSError as e:
                pass
            else:
                print(f'Получен запрос на соединение от {str(addr)}')
                self.clients.append(conn)
            finally:
                wait = 0.2
                r = []
                w = []
                try:
                    r, w, e = select.select(
                        self.clients, self.clients, [], wait)
                except:
                    pass
                requests = self.read_requests(r, self.clients)
                if requests:
                    self.write_response(requests, w, self.clients)

    @staticmethod
    def read_requests(r_clients: list, all_clients: list):
        response = {}
        for sock in r_clients:
            try:
                data = sock.recv(1024).decode('utf-8')
                response[sock] = data
            except:
                print(
                    f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                all_clients.remove(sock)
        return response

    @staticmethod
    def write_response(requests: dict, w_clients: list, all_clients: list):
        for sock_msg in requests:
            for sock_all in all_clients:
                if sock_msg == sock_all:
                    continue
                try:
                    resp = requests[sock_msg].encode('utf-8')
                    sock_all.send(resp)
                except:
                    print(
                        f'Клиент {sock_all.fileno()} {sock_all.getpeername()} отключился')
                    sock_all.close()
                    all_clients.remove(sock_all)


if __name__ == "__main__":
    Server().run_server()
