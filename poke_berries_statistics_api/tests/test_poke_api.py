import os
from unittest.mock import patch

import pytest
import werkzeug

from poke_berries_statistics_api.config import get_poke_api_url
from poke_berries_statistics_api.poke_api import get_berries


class MockResponse:
    next_resp_count = 1

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        MockResponse.next_resp_count = MockResponse.next_resp_count + 1

    def json(self):
        return self.json_data

    def ok(self):
        return self.status_code == 200


def mocked_requests_get(*args, **kwargs):
    poke_api_url = get_poke_api_url()
    if MockResponse.next_resp_count < 4:
        json_data = {
            "count": 3,
            "results": [
                {
                    "name": f"berry {MockResponse.next_resp_count}",
                    "url": f"{poke_api_url}/{MockResponse.next_resp_count}"
                }
            ]
        }
    else:
        json_data = {
            "count": 3,
            "results": []
        }
    return MockResponse(json_data, 200)


def test_get_berries_happy_flow():
    os.environ["POKE_API_PAGE_LIMIT"] = "1"
    with patch('requests.get', side_effect=mocked_requests_get):
        with patch('asyncio.run', side_effect=[
            [{"name": "berry 1", "growth_time": 1}],
            [{"name": "berry 2", "growth_time": 2}],
            [{"name": "berry 3", "growth_time": 3}]
        ]):
            berries = get_berries()

    assert berries.names == ["berry 1", "berry 2", "berry 3"]
    assert berries.growth_times == [1, 2, 3]


def test_poke_api_not_ok():
    def mocked_requests_get_not_ok(*args):
        class MockResponseNotOk:
            def __init__(self):
                self.ok = False
                self.status_code = 404
                self.reason = "Calling PokeAPI fails for some reason."

        return MockResponseNotOk()

    with patch('requests.get', side_effect=mocked_requests_get_not_ok):
        with pytest.raises(werkzeug.exceptions.NotFound):
            get_berries()
