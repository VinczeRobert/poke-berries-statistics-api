import asyncio

import aiohttp
import requests
from flask import abort

from poke_berries_statistics_api.config import get_poke_api_page_limit, get_poke_api_url
from poke_berries_statistics_api.constants import RESULTS, URL, BERRY_NAME, BERRY_GROWTH_TIME
from poke_berries_statistics_api.schemas import BerriesNamesAndGrowthTimesSchema
from poke_berries_statistics_api.utils import execution_time


async def get_berries_concurrently(results):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for result in results:
            berry_response = await session.get(result[URL])
            if not berry_response.ok:
                continue
            tasks.append(berry_response.json())

        return await asyncio.gather(*tasks, return_exceptions=True)


def _get_berries_for_page(offset: int, limit: int) -> BerriesNamesAndGrowthTimesSchema:
    poke_api_base_request = get_poke_api_url()
    response = requests.get(f"{poke_api_base_request}?offset={offset}&limit={limit}")
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
