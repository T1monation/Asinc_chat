import logging
import inspect
import sys


class Log():
    format = logging.Formatter(
        '%(asctime)-10s %(levelname)s %(module)s %(message)s')
    log_to_console = logging.StreamHandler()
    log_to_console.setLevel(logging.DEBUG)
    log_to_console.setFormatter(format)

    log_to_file = logging.FileHandler(
        'test.log', encoding='utf-8')
    log_to_file.setFormatter(format)
    log_to_file.setLevel(logging.DEBUG)

    def __init__(self):
        pass

    def __call__(self, func):
        def decorated(*args, **kwargs):
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back
            code_obj_name = caller_frame.f_code.co_name
            log = logging.getLogger(f'{func.__name__}')
            log.addHandler(self.log_to_console)
            log.addHandler(self.log_to_file)
            log.setLevel(logging.DEBUG)
            log.info(
                f'function {func.__name__} start with args: {args}, kwargs: {kwargs}')
            try:
                result = func(*args, **kwargs)
                log.info(
                    f'starter: {code_obj_name}, function: {func.__name__}, args: {args}, kwargs: {kwargs}, result: {result}')
            except Exception:
                e = sys.exc_info()[1]
                print(e.args[0])
                log.critical(
                    f'somthing goes wrong, exception:{e.args[0]}')
            return result
        return decorated


@Log()
def main(x: int, a=False):
    return x * x


def start():
    main(5)


def wrong():
    main('2')


if __name__ == '__main__':
    main(2, a=True)
    start()
    wrong()
