"""Module for codifying the types of Forecast as an Enum.
"""
from utils.structures.empyrean_enum import EmpyreanEnum


class ForecastType(EmpyreanEnum):
    """A string based enum for codifying the types of forecasts.
    """
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'
