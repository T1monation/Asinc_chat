import subprocess
from time import sleep


"""
Итак, четвертое задание получилось сразу, решил продолжить тему и стазу переделать его в 
задание 5. Идея была такова, что бы получать количество клиентских приложений на чтение чата,
хранить экземпляры объектра Popen() в словаре, где бы ключем выступала строка с названием объекта.
Но, чесно говоря работает данный код только с одним экземпляром,ьвсе остальные не создаються...

"""


def start_subproc(count=1):
    b_client_read = subprocess.Popen('python client_read.py', shell=True)
    print(f"client_read pid: {b_client_read.pid}")
    client_send_dict = {}
    for el in range(count):
        client_send_dict.setdefault(f"client_{el}", subprocess.call(
            'python client_send.py', shell=True))

    # c_client_send = subprocess.Popen('python client_send.py', shell=True)
    # print(f"client_send pid: {c_client_send.pid}")
    sleep(5)
    del_set = set()
    while True:
        for el in client_send_dict:
            if client_send_dict[el] == 0:
                del_set.add(el)
        if len(del_set) == count:
            print('created clients: \n', client_send_dict)
            b_client_read.kill()
            print('sucsess')
            exit(0)


count = int(input('введите количество клиентов: '))
start_subproc()
