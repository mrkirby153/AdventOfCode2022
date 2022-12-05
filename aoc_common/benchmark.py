import time
from functools import wraps


def print_timing(func: callable) -> callable:
    """
    Decorator to output the time it took for the function to run
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        print(f"{func.__name__} took {(end - start) / 1000000:0.1f} ms")
        return result
    return wrapper
