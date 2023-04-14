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


def msg_sender(action='msg', encoding='utf-8', text_msg=''):
    if action == 'presense':
        msg = {
            "action": action,
            "time": time.time(),
            "type": "status online"
        }
    if action == 'msg':
        if text_msg == '':
            text_msg = str(input('message to server: '))
        msg = {
            "action": action,
            "time": time.time(),
            "text message": text_msg
        }

    return json.dumps(msg).encode(encoding)


def incoming_msg(data, encoding='utf-8'):
    json_data = json.loads(data.decode(encoding))
    try:
        return f'server status {json_data["response"]}, {json_data["alert"]}'
    except KeyError:
        return 'wrong incoming message'


def main():
    args = parser()
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((args.addr, args.port))

    client.send(msg_sender(action='presense'))

    while True:
        client.send(msg_sender())
        data = client.recv(1024)
        print(incoming_msg(data))


if __name__ == '__main__':
    main()
