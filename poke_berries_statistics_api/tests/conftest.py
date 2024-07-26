import pytest

from poke_berries_statistics_api.api import app


@pytest.fixture()
def flask_client():
    app.config['TESTING'] = True
    return app.test_client()
