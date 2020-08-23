from functools import wraps
from time import sleep


def retry_on_network_errors(times):
    def wrapper_fn(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            err = None
            for _ in range(times):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    err = e
                    print(f"Error, `{e}`")
                    sleep(0.1)
            raise err
        return wrapper
    return wrapper_fn
