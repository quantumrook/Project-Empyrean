from enum import Enum


class RequestType(Enum):
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

    @classmethod
    def list(cls) -> list:
        """
        Returns all of the widget types as a list.

        Source: https://stackoverflow.com/a/54919285
        """
        return list(map(lambda c: c.value, cls))
