import time
from functools import wraps

from poke_berries_statistics_api.config import get_calculate_time


def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        calculate_time = get_calculate_time()
        if calculate_time:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f'Function {func.__name__} took {total_time:.4f} seconds.')
            return result
        else:
            return func(*args, **kwargs)
    return wrapper
