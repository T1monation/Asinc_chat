# Задание 2.
import json
from mimesis import Person, Finance, Hardware, Datetime
from random import randint


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date,
    }
    with open('orders.json', 'a', encoding='utf-8') as f:
        json.dump(dict_to_json, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    person = Person()
    hardware = Hardware()
    finance = Finance()
    datetame = Datetime()
    for i in range(10):
        write_order_to_json(hardware.graphics(), randint(
            1, 10), finance.price(), person.full_name(), datetame.formatted_date())
