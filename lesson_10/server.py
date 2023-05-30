import select
from socket import *
from metaclass import ClassVerifier, PortChecker


class Server(metaclass=ClassVerifier):
    clients = []
    port = PortChecker()
    socket = socket()

    def __init__(self, ip_addr='localhost', port=7777, max_clients=5, timeout=0.2):
        self.ip_addr = ip_addr
        self.port = port
        self.max_clients = max_clients
        self.timeout = timeout

    def run_server(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.ip_addr, self.port))
        self.socket.listen(self.max_clients)
        self.socket.settimeout(self.timeout)

        while True:
            try:
                conn, addr = self.socket.accept()
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
