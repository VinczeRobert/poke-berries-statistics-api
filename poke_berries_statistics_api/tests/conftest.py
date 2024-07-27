import os
import shutil

import pytest

from poke_berries_statistics_api.api import app
from poke_berries_statistics_api.config import get_caching_dir


@pytest.fixture(scope='session')
def flask_client():
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture()
def empty_cache():
    caching_dir = get_caching_dir()
    if os.path.exists(caching_dir):
        shutil.rmtree(caching_dir)
