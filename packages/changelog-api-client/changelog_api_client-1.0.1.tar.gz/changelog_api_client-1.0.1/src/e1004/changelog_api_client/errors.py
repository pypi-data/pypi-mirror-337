from requests.exceptions import HTTPError


def handle_error(func, *args, **kwargs):
    try:
        print(func(*args, **kwargs))
    except HTTPError as err:
        code = str(err.response.status_code)
        if code.startswith("4"):
            payload = err.response.json()
            print(f"{code} {payload}")
            return
        raise
