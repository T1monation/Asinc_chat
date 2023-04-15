from socket import *
import time
import json
import argparse
import logging
import log.client_log_config
import traceback


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
    log = logging.getLogger('client')
    json_data = json.loads(data.decode(encoding))
    try:
        log.info(
            f'incoming message, server status {json_data["response"]}, {json_data["alert"]} ')
        return f'server status {json_data["response"]}, {json_data["alert"]}'
    except KeyError:
        log.critical(f'error: {traceback.format_exc()}')
        return 'wrong incoming message'


def main():
    log = logging.getLogger('client')
    args = parser()
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((args.addr, args.port))
    log.info(f'starting whith server addres {args.addr} port {args.port}')
    client.send(msg_sender(action='presense'))

    while True:
        client.send(msg_sender())
        data = client.recv(1024)
        incoming_msg(data)


if __name__ == '__main__':
    main()
