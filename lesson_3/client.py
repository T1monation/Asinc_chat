from socket import *
import time
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Client message app")
    parser.add_argument('--port', metavar='--p', type=int,
                        help='server TCP-port', default=7777)
    parser.add_argument('--addr', metavar='--a', type=str,
                        help='server address', default='localhost')
    args = parser.parse_args()

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((args.addr, args.port))
    presense_msg = {
        "action": "presense",
        "time": time.time(),
        "type": "status online"
    }
    client.send(json.dumps(presense_msg).encode('utf-8'))

    while True:
        msg = str(input('message to server: '))
        msg_to_server = {
            "action": "msg",
            "time": time.time(),
            "text message": msg
        }
        client.send(json.dumps(msg_to_server).encode('utf-8'))
        data = client.recv(1024)
        json_data = json.loads(data.decode('utf-8'))
        print(f'server status {json_data["response"]}, {json_data["alert"]} ')


if __name__ == '__main__':
    main()
