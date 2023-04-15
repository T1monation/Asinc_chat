from socket import *
import time
import json


def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('localhost', 7777))

    client.send(json.dumps({
                "time": time.time(),
                "text message": "oops!"
                }).encode('utf-8'))


if __name__ == '__main__':
    main()
