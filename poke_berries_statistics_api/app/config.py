import logging
import os

from dotenv import load_dotenv

load_dotenv()


def _string_to_bool(string):
    if isinstance(string, bool):
        return string
    string = string.lower()
    return True if string in ['true', '1', 'y', 'yes'] else False


def get_poke_api_page_limit() -> int:
    return int(os.environ.get("POKE_API_PAGE_LIMIT", 20))


def get_calculate_time() -> bool:
    return _string_to_bool(os.environ.get("CALCULATE_TIME", "False"))


def get_poke_api_url() -> str:
    return os.environ.get("POKE_API_URL", "https://pokeapi.co/api/v2/berry")


def get_logs_level() -> int:
    level_as_str = os.environ.get("LOGS_LEVEL", "INFO")
    if level_as_str == "DEBUG":
        return logging.DEBUG
    elif level_as_str == "INFO":
        return logging.INFO
    elif level_as_str == "WARNING":
        return logging.WARN
    elif level_as_str == "ERROR":
        return logging.ERROR
    else:
        return logging.CRITICAL


def get_reset_logs() -> bool:
    return _string_to_bool(os.environ.get("RESET_LOGS", False))


def get_caching_dir() -> str:
    return os.environ.get("CACHING_DIR", 'cache_files')
