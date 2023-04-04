# Задание 5.
import subprocess

args = ['ping', 'yandex.ru']
args_2 = ['ping', 'youtube.com']

subproc_ping_1 = subprocess.Popen(args, stdout=subprocess.PIPE)
for line_1 in subproc_ping_1.stdout:
    print(line_1.decode('utf-8') + 'яндекс жив')
    # Ограничим для linux-консоли количество повторений
    if 'icmp_seq=4' in line_1.decode('utf-8'):
        break

subproc_ping_2 = subprocess.Popen(args_2, stdout=subprocess.PIPE)
for line_2 in subproc_ping_2.stdout:
    print(line_2.decode('utf-8') + 'ютубчик на проводе')
    if 'icmp_seq=4' in line_2.decode('utf-8'):
        break
