from unittest.mock import Mock, patch

from poke_berries_statistics_api.schemas import BerryStatsResponse, BerriesNamesAndGrowthTimesSchema


def test_berries(flask_client):
    berries_response = BerriesNamesAndGrowthTimesSchema(
        names=["berry 1", "berry 2", "berry 3"],
        growth_times=[3, 18, 3]
    )
    berry_stats_response = BerryStatsResponse(
        berries_names=["berry 1", "berry 2", "berry 3"],
        min_growth_time=3,
        max_growth_time=18,
        median_growth_time=6.0,
        mean_growth_time=9.0,
        variance_growth_time=42.0,
        frequency_growth_time={3: 1, 6: 1, 18: 1}
    )

    with patch('poke_berries_statistics_api.api.get_berries',
               side_effect=Mock(return_value=berries_response)) as mocked_get_berries:
        with patch('poke_berries_statistics_api.api.calculate_berry_stats',
                   side_effect=Mock(return_value=berry_stats_response)) as mocked_calculate_berry_stats:
            response = flask_client.get('/allBerryStats')

    assert response.status_code == 200
    mocked_get_berries.assert_called_with()
    mocked_calculate_berry_stats.assert_called_with(berries_response)
    berry_stats_response.frequency_growth_time = \
        {str(key): value for key, value in berry_stats_response.frequency_growth_time.items()}
    assert response.json == berry_stats_response.dict()
