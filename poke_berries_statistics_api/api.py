import logging

from flask import make_response, render_template
from waitress import serve

from poke_berries_statistics_api.flask_app import app, cache
from poke_berries_statistics_api.poke_api import get_berries
from poke_berries_statistics_api.service import calculate_berry_stats, create_histogram
from poke_berries_statistics_api.utils import setup_logging

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


@app.route("/histogram", methods=['GET'])
@cache.cached(timeout=120)
def get_histogram():
    logger.info("GET /histogram endpoint called.")
    berries = get_berries()
    create_histogram(berries.growth_times)
    logger.info("GET /histogram endpoint successfully completed.")
    return render_template('histogram.html')


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
