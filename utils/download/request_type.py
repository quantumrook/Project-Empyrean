from enum import Enum

class RequestType(Enum):
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

    def get_list_of_types() -> list:
        return [RequestType.POINTS, RequestType.HOURLY, RequestType.EXTENDED]