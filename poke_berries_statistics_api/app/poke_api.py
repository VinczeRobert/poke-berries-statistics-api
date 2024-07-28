import asyncio
import logging

import aiohttp
import requests
from flask import abort

from poke_berries_statistics_api.app.config import get_poke_api_page_limit, get_poke_api_url
from poke_berries_statistics_api.app.constants import RESULTS, URL, BERRY_NAME, BERRY_GROWTH_TIME
from poke_berries_statistics_api.app.flask_app import cache
from poke_berries_statistics_api.app.schemas import BerriesNamesAndGrowthTimesSchema
from poke_berries_statistics_api.app.utils import execution_time

logger = logging.getLogger(__name__)


def _get_poke_api_request_url(offset, limit):
    base_request_url = get_poke_api_url()
    return f"{base_request_url}?offset={offset}&limit={limit}"


async def get_berries_concurrently(results):  # pragma: no cover
    async with aiohttp.ClientSession() as session:
        tasks = []
        for result in results:
            logger.debug(f"Calling {result[URL]}")
            berry_response = await session.get(result[URL])
            if berry_response.ok:
                tasks.append(berry_response.json())
            else:
                error_message = (f"An unexpected error has appeared when calling {result[URL]}."
                                 f" The error is: {berry_response.reason}")
                logger.error(error_message)
                abort(berry_response.status, error_message)

        return await asyncio.gather(*tasks, return_exceptions=True)


def _get_berries_for_page(offset: int, limit: int) -> BerriesNamesAndGrowthTimesSchema:
    poke_api_request_url = _get_poke_api_request_url(offset, limit)
    response = requests.get(poke_api_request_url)
    if not response.ok:
        abort(response.status_code, response.reason)

    response_json = response.json()
    results = response_json[RESULTS]

    if len(results) == 0:
        return BerriesNamesAndGrowthTimesSchema(
            names=[],
            growth_times=[]
        )

    responses = asyncio.run(get_berries_concurrently(results=results))

    berry_names = [resp[BERRY_NAME] for resp in responses]
    berry_growth_times = [resp[BERRY_GROWTH_TIME] for resp in responses]

    return BerriesNamesAndGrowthTimesSchema(
        names=berry_names,
        growth_times=berry_growth_times
    )


@execution_time
@cache.cached(timeout=120, key_prefix='all_berries')
def get_berries() -> BerriesNamesAndGrowthTimesSchema:
    offset = 0
    limit = get_poke_api_page_limit()
    berry_names = []
    berry_growth_times = []

    berries_for_page = _get_berries_for_page(offset, limit)
    berry_names.extend(berries_for_page.names)
    berry_growth_times.extend(berries_for_page.growth_times)

    while len(berries_for_page.names) > 0:
        offset = offset + limit
        berries_for_page = _get_berries_for_page(offset, limit)
        berry_names.extend(berries_for_page.names)
        berry_growth_times.extend(berries_for_page.growth_times)

    return BerriesNamesAndGrowthTimesSchema(
        names=berry_names,
        growth_times=berry_growth_times
    )
