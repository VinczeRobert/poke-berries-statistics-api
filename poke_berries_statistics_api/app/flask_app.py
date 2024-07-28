from flask import Flask
from flask_caching import Cache

from poke_berries_statistics_api.app.config import get_caching_dir

config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": 120,
    "CACHE_DIR": get_caching_dir(),
    "CACHE_THRESHOLD": 10,
}
app = Flask(__name__, static_folder='templates/static')
app.config.from_mapping(config)

cache = Cache(app)
