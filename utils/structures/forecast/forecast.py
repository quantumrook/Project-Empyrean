from dataclasses import dataclass
from typing import Any

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.forecast_data import ForecastData


@dataclass
class Forecast():
    units           : str
    generatedAt     : EmpyreanDateTime
    updateTime      : EmpyreanDateTime
    validTimes      : EmpyreanDateTime

    forecasts       : dict[EmpyreanDateTime, ForecastData]

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.units = forecast_data["units"]
        self.generatedAt = EmpyreanDateTime(generating_str=forecast_data["generatedAt"])
        self.updateTime =  EmpyreanDateTime(generating_str=forecast_data["updateTime"])
        self.validTimes = EmpyreanDateTime(generating_str=forecast_data["validTimes"])
        self.forecasts = { }
        for period in forecast_data["periods"]:
            forecast = ForecastData(period)
            self.forecasts[forecast.startTime] = forecast