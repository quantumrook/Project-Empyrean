"""Helper enum for codifying the API Request types.
"""
from utils.structures.empyrean_enum import EmpyreanEnum


class RequestType(EmpyreanEnum):
    """The types of requests possible to query the NWS API with.
    """
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'
