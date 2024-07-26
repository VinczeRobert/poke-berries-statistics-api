import os

from dotenv import load_dotenv

load_dotenv()


def _string_to_bool(string):
    string = string.lower()
    return True if string in ['true', '1', 'y', 'yes'] else False


def get_poke_api_page_limit() -> int:
    return int(os.environ.get("POKE_API_PAGE_LIMIT", 20))


def get_calculate_time() -> bool:
    return _string_to_bool(os.environ.get("CALCULATE_TIME", "False"))


def get_poke_api_url() -> str:
    return os.environ.get("POKE_API_URL", "https://pokeapi.co/api/v2/berry")
