# Task 1: Writing and Testing a Decorator
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        # Log function name, arguments, and return value
        result = func(*args, **kwargs)
        log_message = (
            f"function: {func.__name__} "
            f"positional parameters: {list(args) if args else 'none'} "
            f"keyword parameters: {dict(kwargs) if kwargs else 'none'} "
            f"return: {result}"
        )
        logger.log(logging.INFO, log_message)
        return result
    return wrapper

@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def check_args(*args):
    return True

@logger_decorator
def check_kwargs(**kwargs):
    return "Processed kwargs"

if __name__ == "__main__":
    say_hello()
    check_args(1, 2, 3)
    check_kwargs(name="Alice", age=30)