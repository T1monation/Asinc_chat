from socket import *
import time
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Server message app")
    parser.add_argument('--port', metavar='--p', type=int,
                        help='server TCP-port', default=7777)
    parser.add_argument('--addr', metavar='--a', type=str,
                        help='server address', default='localhost')
    args = parser.parse_args()

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((args.addr, args.port))
    server.listen(5)

    client, addr = server.accept()
    print(f'start connection on address: {addr}')

    while True:
        data = client.recv(100000)
        json_data = json.loads(data.decode('utf-8'))
        if json_data["action"] == "presense":
            print('client status: ', json_data["type"])
        if json_data["action"] == "msg":
            print('input message: ', json_data["text message"])
        msg = {
            "response": 200,
            "time": time.time(),
            "alert": "message recived"
        }
        client.send(json.dumps(msg).encode('utf-8'))


if __name__ == '__main__':
    main()
