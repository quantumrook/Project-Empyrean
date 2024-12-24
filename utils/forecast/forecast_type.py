from enum import Enum

class ForecastType(Enum):
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

    def get_list_of_types() -> list:
        return [ForecastType.HOURLY, ForecastType.EXTENDED]