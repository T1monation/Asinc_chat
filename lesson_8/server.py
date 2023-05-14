import select
from socket import *


def read_requests(r_clients: list, all_clients: list):

    response = {}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            response[sock] = data
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)

    return response


def write_response(requests: dict, w_clients: list, all_clients: list):
    # print('111111111111111\n', requests)

    for sock_msg in requests:
        for sock_all in all_clients:
            if sock_msg == sock_all:
                continue
            try:
                # print(requests[sock_w])c
                resp = requests[sock_msg].encode('utf-8')
                sock_all.send(resp)
            except:
                print(
                    f'Клиент {sock_all.fileno()} {sock_all.getpeername()} отключился')
                sock_all.close()
                all_clients.remove(sock_all)


def mainloop():

    address = ('localhost', 10000)
    clients = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)

    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            print(f'Получен запрос на соединение от {str(addr)}')
            clients.append(conn)
        finally:
            wait = 0.2
            r = []
            w = []

            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_response(requests, w, clients)


if __name__ == '__main__':
    print('Сервер запущен')
    mainloop()
