# Задание 3.
import yaml
from yaml import Loader


some_dict = {"🐨": ['el1', 'el2'],
             '🐧': 155,
             '🐽': {
    'el_1': '1',
    'el_2': '2',
},
}

with open('test.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(some_dict, f, default_flow_style=False, allow_unicode=True)


with open('test.yaml', 'r', encoding='utf-8') as fl:
    load_data = yaml.load(fl, Loader=Loader)
    print(load_data)


try:
    assert some_dict == load_data
    print('Данные совпадают!')
except AssertionError:
    print('Заданный и загруженный словари не совпадают')
    exit(1)
