import pytest

from poke_berries_statistics_api.app.service import calculate_berry_stats
from poke_berries_statistics_api.app.schemas import BerriesNamesAndGrowthTimesSchema, BerryStatsResponse


def _get_test_data_1():
    test_input = BerriesNamesAndGrowthTimesSchema(
        names=["berry 1", "berry 2", "berry 3"],
        growth_times=[3, 6, 18]
    )
    test_output = BerryStatsResponse(
        berries_names=["berry 1", "berry 2", "berry 3"],
        min_growth_time=3,
        max_growth_time=18,
        median_growth_time=6.0,
        mean_growth_time=9.0,
        variance_growth_time=42.0,
        frequency_growth_time={3: 1, 6: 1, 18: 1}
    )

    return {
        "input": test_input,
        "output": test_output,
    }


def _get_test_data_2():
    test_input = BerriesNamesAndGrowthTimesSchema(
        names=["berry 1", "berry 2", "berry 3"],
        growth_times=[5, 7, 5]
    )
    test_output = BerryStatsResponse(
        berries_names=["berry 1", "berry 2", "berry 3"],
        min_growth_time=5,
        max_growth_time=7,
        median_growth_time=5,
        mean_growth_time=5.6666667,
        variance_growth_time=0.88888889,
        frequency_growth_time={5: 2, 7: 1}
    )

    return {
        "input": test_input,
        "output": test_output,
    }


def _get_test_data_3():
    test_input = BerriesNamesAndGrowthTimesSchema(
        names=["berry 1", "berry 2", "berry 3", "berry 4", "berry 5", "berry 6", "berry 7", "berry 8", "berry 9",
               "berry 10"],
        growth_times=[1, 4, 5, 1, 2, 7, 8, 3, 8, 6]
    )
    test_output = BerryStatsResponse(
        berries_names=["berry 1", "berry 2", "berry 3", "berry 4", "berry 5", "berry 6", "berry 7", "berry 8",
                       "berry 9", "berry 10"],
        min_growth_time=1,
        max_growth_time=8,
        median_growth_time=4.5,
        mean_growth_time=4.5,
        variance_growth_time=6.65,
        frequency_growth_time={1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 2}
    )

    return {
        "input": test_input,
        "output": test_output,
    }


@pytest.mark.parametrize("test_data", [_get_test_data_1(), _get_test_data_2(), _get_test_data_3()])
def test_calculate_berry_stats(test_data):
    actual_result = calculate_berry_stats(test_data["input"])
    expected_result = test_data["output"]

    assert actual_result.berries_names == expected_result.berries_names, "berries_names has incorrect value"
    assert actual_result.min_growth_time == expected_result.min_growth_time, "min_growth_time has incorrect value"
    assert actual_result.max_growth_time == expected_result.max_growth_time, "max_growth_time has incorrect value"
    assert actual_result.median_growth_time == expected_result.median_growth_time, \
        "median_growth_time has incorrect value"
    assert pytest.approx(actual_result.mean_growth_time, 0.0001) == expected_result.mean_growth_time,\
        "mean_growth_time has incorrect value"
    assert pytest.approx(actual_result.variance_growth_time, 0.0001) == expected_result.variance_growth_time, \
        "variance_growth_time has incorrect value"
    assert actual_result.frequency_growth_time == expected_result.frequency_growth_time, \
        "frequency_growth_time has incorrect value"
