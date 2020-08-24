from functools import wraps
from time import sleep, time
from requests.exceptions import HTTPError


def retry_on_network_errors(times=5):
    def wrapper_fn(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            err = None
            for _ in range(times):
                try:
                    return f(*args, **kwargs)
                except HTTPError as e:
                    if e.response.status_code >= 500:
                        err = e
                        print(f"Error, `{e}`")
                        sleep(0.1)
                    else:
                        raise err
        return wrapper
    return wrapper_fn


def refresh_access_token(f):
    @wraps(f)
    def wrapper(slf, *args, **kwargs):
        if time() > slf.token_expire_time:
            slf._retrieve_access_token_data()
        return f(slf, *args, **kwargs)
    return wrapper
