import select
from socket import *
from metaclass import ClassVerifier, PortChecker
import logging
import sys
import argparse
from models import Client, engine, History
from sqlalchemy.orm import Session
import json
from sqlalchemy import select as SEL
import time


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
                self.wait = 0.2
                self.r = []
                self.w = []
                try:
                    self.r, self.w, e = select.select(
                        self.clients, self.clients, [], self.wait)
                except:
                    pass
                # print('call read_response')
                requests = self.read_requests
                if requests:
                    self.write_response(requests)

    @property
    def read_requests(self):
        response = {}
        for sock in self.r:
            try:
                data = sock.recv(1024).decode('utf-8')
            except:
                pass
                # with Session(engine) as s:
                #     #  при отключении клиента по его адресу и порту находим в БД запись
                #     #  очищаем data, убираем статус онлайн
                #     find_client = s.scalar(
                #         SEL(Client).where(Client.data == str(sock.getpeername())))
                #     find_client.status_online = False

                #     find_client.data = None

                #     s.commit()

                #     print(
                #         f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                #     sock.close()
                #     all_clients.remove(sock)
            else:
                check_sock, check_data = self.data_analisis(sock, data)
                response[check_sock] = check_data
                print(response)

        return response

    def write_response(self, requests: dict):
        for sock_msg in requests:
            for sock in self.w:
                if sock_msg == sock:
                    continue
                try:
                    resp = requests[sock_msg].encode('utf-8')
                    sock.send(resp)
                except:
                    with Session(engine) as s:
                        #  при отключении клиента по его адресу и порту находим в БД запись
                        #  очищаем data, убираем статус онлайн
                        find_client = s.scalar(
                            SEL(Client).where(Client.data == str(sock_msg.getpeername())))
                        find_client.status_online = False
                        find_client.data = None

                        s.commit()

                    print(
                        f'Клиент {sock_msg.fileno()} {sock_msg.getpeername()} отключился')
                    sock.close()
                    self.clients.remove(sock)

    def data_analisis(self, sock,  data):
        """
        data_analisis - метод - "перехватчик", анализирует сообщения,
        пользовательские пересылает без изменений, системные обрабатывает,
        """
        # False - сообщения для сервера, передаче пользователям не подлежит
        self.return_flag = False

        try:
            ansver = json.loads(data)

        except json.decoder.JSONDecodeError as e:
            pass
        else:
            if ansver["action"] == 'msg':
                # Устанавливаем True если сообщение другим пользователям
                self.return_flag = True
                user = ansver["name"]
                with Session(engine) as s:

                    _find_login = s.scalar(
                        SEL(Client).where(Client.login.in_([user,])))

                    # Создаем первичную запись о клиенте, если клиента с таким логином еще не существовало
                    if not _find_login:
                        _client = Client(
                            login=ansver["name"],
                            #  в data храним адрес и порт для идентификации клиента и его соединения
                            data=str(sock.getpeername()),
                            status_online=True
                        )
                        # применяем изменения в БД
                        s.add(_client)
                        s.commit()

                    else:
                        # обновляем для уже существующего клиента data в БД
                        _find_login.data = str(sock.getpeername())
                        _find_login.status_online = True

                    # Для каждого пакета будем писать историю:
                    _history = History(
                        client_login=ansver["name"],
                        client_ip=sock.getpeername(),
                        # Долой приватность, пишим все к себе в базу!!!
                        client_message=ansver["msg"]
                    )

                    s.add(_history)
                    s.commit()


            elif ansver["action"] == "get_contacts":

                with Session(engine) as s:
                    find_list = s.execute(SEL(Client.login).where(
                        Client.status_online == True)).all()
                    cli_list = [el[0] for el in find_list]

                    ansver = {'name': 'server',
                              'msg': cli_list,
                              'action': 'list',
                              'time': time.time(), }


                return sock, json.dumps(ansver)

        finally:
            if self.return_flag:
                return sock, data


if __name__ == "__main__":
    Server().run_server()
