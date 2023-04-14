import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


format = logging.Formatter(
    '%(asctime)-10s %(levelname)s %(module)s %(message)s')

log = logging.getLogger('server')

# Для наглядности отклоняюсь то ДЗ, и ввожу ротацию лог-файлов каждую минуту
f = TimedRotatingFileHandler(
    'server.log', encoding='utf-8', when='M', interval=1)
f.setFormatter(format)
f.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(format)

log.addHandler(f)
log.addHandler(console)
log.setLevel(logging.DEBUG)
