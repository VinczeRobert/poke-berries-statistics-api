import logging

from flask import Flask, make_response
from flask_caching import Cache

from poke_berries_statistics_api.config import get_caching_dir
from poke_berries_statistics_api.poke_api import get_berries
from poke_berries_statistics_api.service import calculate_berry_stats
from poke_berries_statistics_api.utils import setup_logging

config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": 120,
    "CACHE_DIR": get_caching_dir(),
    "CACHE_THRESHOLD": 10,
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

setup_logging()
logger = logging.getLogger(__name__)


@app.route("/allBerryStats", methods=['GET'])
@cache.cached(timeout=120)
def get_all_berry_stats():
    logger.info("GET /allBerryStats endpoint called.")
    berries = get_berries()
    berry_stats = calculate_berry_stats(berries)

    response = make_response(berry_stats.json())
    response.headers['Content-Type'] = 'application/json'
    logger.info("GET /allBerryStats endpoint successfully completed.")
    return response
