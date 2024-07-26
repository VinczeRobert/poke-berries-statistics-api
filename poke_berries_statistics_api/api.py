from flask import Flask, make_response

from poke_berries_statistics_api.poke_api import get_berries
from poke_berries_statistics_api.service import calculate_berry_stats

app = Flask(__name__)


@app.route("/allBerryStats", methods=['GET'])
def get_all_berry_stats():
    berries = get_berries()
    berry_stats = calculate_berry_stats(berries)

    response = make_response(berry_stats.json())
    response.headers['Content-Type'] = 'application/json'
    return response
