import logging
import time
from functools import wraps

from poke_berries_statistics_api.config import get_calculate_time, get_logs_level, get_reset_logs

logger = logging.getLogger(__name__)


def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        calculate_time = get_calculate_time()
        if calculate_time:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logger.info(f'Function {func.__name__} took {total_time:.4f} seconds.')
            return result
        else:
            return func(*args, **kwargs)
    return wrapper


def setup_logging():
    level = get_logs_level()
    filemode = 'w' if get_reset_logs() else 'a'
    logs_format = '%(name)s:%(levelname)s:%(asctime)s:%(message)s'
    logging.basicConfig(level=level, filename='poke_berries_statistics.log', filemode=filemode, format=logs_format)
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.ERROR)
