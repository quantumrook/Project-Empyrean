from dataclasses import dataclass
from typing import Any

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.temperature import Temperature
from utils.structures.forecast.wind import Wind


@dataclass
class ForecastData():
    number                      : int
    name                        : str
    startTime                   : EmpyreanDateTime
    endTime                     : EmpyreanDateTime
    isDaytime                   : bool
    temperature                 : Temperature
    probabilityOfPrecipitation  : int
    wind                        : Wind
    icon                        : str
    short                       : str
    detailed                    : list[str]

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.number = forecast_data["number"]
        self.name = forecast_data["name"]
        self.startTime = EmpyreanDateTime(generating_str=forecast_data["startTime"])
        self.endTime = EmpyreanDateTime(generating_str=forecast_data["endTime"])
        self.isDaytime = bool(forecast_data["isDaytime"])
        self.temperature = Temperature(forecast_data)
        self.probabilityOfPrecipitation = forecast_data["probabilityOfPrecipitation"]["value"]
        self.wind = Wind(forecast_data)
        self.icon = forecast_data["icon"]
        self.short = forecast_data["shortForecast"]
        detailed_with_sep = forecast_data["detailedForecast"].replace('.', './')
        self.detailed = [line for line in detailed_with_sep.split('/')]
    