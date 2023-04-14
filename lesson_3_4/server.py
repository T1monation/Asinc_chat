from socket import *
import time
import json
import argparse


def parser():
    parser = argparse.ArgumentParser(description="Server message app")
    parser.add_argument('--port', metavar='--p', type=int,
                        help='server TCP-port', default=7777)
    parser.add_argument('--addr', metavar='--a', type=str,
                        help='server address', default='localhost')
    return parser.parse_args()


def data_loads(data,  decoding='utf-8'):
    json_data = json.loads(data.decode(decoding))
    try:
        if json_data["action"] == "presense":
            return f'client status: {json_data["type"]}'
        if json_data["action"] == "msg":
            return f'input message: {json_data["text message"]}'
    except KeyError:
        return 'Invalid message!'


def server_answer(encoding='utf-8', response=200, text_msg='message recived'):
    msg = {
        "response": response,
        "time": time.time(),
        "alert": text_msg
    }
    return json.dumps(msg).encode(encoding)


def main():
    args = parser()
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((args.addr, args.port))
    server.listen(5)

    client, addr = server.accept()
    print(f'start connection on address: {addr}')

    while True:
        data = client.recv(100000)
        print(data_loads(data))
        client.send(server_answer())


if __name__ == '__main__':
    main()
