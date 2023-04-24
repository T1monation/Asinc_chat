import logging


format = logging.Formatter(
    '%(asctime)-10s %(levelname)s %(module)s %(message)s')

log = logging.getLogger('client')

f = logging.FileHandler('client.log', encoding='utf-8')
f.setFormatter(format)
f.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(format)

log.addHandler(f)
log.addHandler(console)
log.setLevel(logging.DEBUG)
