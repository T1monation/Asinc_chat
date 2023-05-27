import ipaddress
import platform
import subprocess
import re
from tabulate import tabulate


def check_host_ping(ip_list: list):
    '''
Не знаю, прочтет ли кто-нибудь эти строки, учитывая, что срок здачи ДЗ пропущен,
но все же... 
Крепко подумав, и еще больше прогуглив, я так и не понял, КАК, а самое гланое ЗАЧЕМ
прикручивать  ipaddress для решения данного задания, учитывая что он в принципе не
работает с именами хостов??? Есть решения с помощью requests и socket, но мне 
понравилось решение myping()
'''
    for el in ip_list:
        print(myping(el))


def host_range_ping():
    '''
    И в этом задании чесно говоря не вижу смысла особого применять ipaddress...
    Мне как то не очень понравилась во время моих экспириментов работа  ip_network()
    и ее переборка, как было заявленно в методичке
    '''
    ip_addr = input('Введите IP-адрес: ')
    start_range = int(input('Введите начало диапазона проверки адресов: '))
    end_range = int(input('Введите конец диапазона проверки адресов: '))
    find_ip = re.search(r'\d{1,}\.\d{1,}\.\d{1,}\.', ip_addr)
    for el in range(start_range, end_range):
        print(myping(f'{find_ip[0]}{el}'))


def host_range_ping_tab():
    result_dict = {'Узел доступен': [], 'Узел недоступен': []}
    ip_addr = input('Введите IP-адрес: ')
    start_range = int(input('Введите начало диапазона проверки адресов: '))
    end_range = int(input('Введите конец диапазона проверки адресов: '))
    find_ip = re.search(r'\d{1,}\.\d{1,}\.\d{1,}\.', ip_addr)
    for el in range(start_range, end_range):
        result = myping(f'{find_ip[0]}{el}')
        if result == 'Узел доступен':
            result_dict['Узел доступен'].append(f'{find_ip[0]}{el}')
        else:
            result_dict['Узел недоступен'].append(f'{find_ip[0]}{el}')
    print(tabulate(result_dict, headers='keys',
          tablefmt='pipe', stralign='center'))


def myping(host):
    parameter = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)
    if response == 0:
        return 'Узел доступен'
    else:
        return 'Узел недоступен'


if __name__ == '__main__':
    # Задание 1:
    # ip_list = [
    #     '192.168.1.1',
    #     '192.168.1.10',
    #     '10.10.1.5',
    #     'ya.ru',
    #     'google.com',
    # ]
    # check_host_ping(ip_list)
    # Задание 2:
    # host_range_ping()
    # Задание 3:
    host_range_ping_tab()
