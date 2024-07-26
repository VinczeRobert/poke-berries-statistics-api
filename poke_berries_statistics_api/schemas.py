from typing import Dict, List

from pydantic import BaseModel


class BerriesNamesAndGrowthTimesSchema(BaseModel):
    names: List[str]
    growth_times: List[int]


class BerryStatsResponse(BaseModel):
    berries_names: List[str]
    min_growth_time: int
    max_growth_time: int
    median_growth_time: int | float
    mean_growth_time: float
    variance_growth_time: float
    frequency_growth_time: Dict[int, int]
