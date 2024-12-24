from enum import Enum

class ForecastType(Enum):
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

    def get_list_of_types(self) -> list:
        return [ForecastType.POINTS, ForecastType.HOURLY, ForecastType.EXTENDED]