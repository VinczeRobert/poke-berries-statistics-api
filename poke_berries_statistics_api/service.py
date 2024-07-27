from typing import List, Dict

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from poke_berries_statistics_api.schemas import BerryStatsResponse, BerriesNamesAndGrowthTimesSchema
from poke_berries_statistics_api.utils import execution_time

matplotlib.use('Agg')


def _calculate_frequency_growth_time(growth_times: List[int]) -> Dict[int, int]:
    freq_dict = dict()

    for g_time in growth_times:
        freq = freq_dict.setdefault(g_time, 0)
        freq_dict[g_time] = freq + 1

    return freq_dict


@execution_time
def calculate_berry_stats(berries: BerriesNamesAndGrowthTimesSchema) -> BerryStatsResponse:
    growth_times = berries.growth_times
    max_growth_time = max(growth_times)
    min_growth_time = min(growth_times)
    median_growth_time = np.median(growth_times)
    mean_growth_time = np.mean(growth_times)
    variance_growth_time = np.var(growth_times)
    frequency_growth_time = _calculate_frequency_growth_time(growth_times)

    return BerryStatsResponse(
        berries_names=berries.names,
        min_growth_time=min_growth_time,
        max_growth_time=max_growth_time,
        median_growth_time=float(median_growth_time),
        mean_growth_time=float(mean_growth_time),
        variance_growth_time=float(variance_growth_time),
        frequency_growth_time=frequency_growth_time
    )


@execution_time
def create_histogram(berry_growth_times: List) -> None:
    plt.hist(berry_growth_times, 10)
    plt.savefig('poke_berries_statistics_api/templates/static/histogram.png')
