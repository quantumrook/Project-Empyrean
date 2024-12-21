from dataclasses import dataclass
from typing import Any

from gui.empyrean.datetime import *

@dataclass
class TemperatureData():
    value       : int
    unit        : str
    trend       : str

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.value = forecast_data["temperature"]
        self.unit = forecast_data["temperatureUnit"]
        self.trend = forecast_data["temperatureTrend"]

@dataclass
class WindData():
    value       : int
    unit        : str
    direction   : str

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.value, self.unit = forecast_data["windSpeed"].split(' ')
        self.direction = forecast_data["windDirection"]

@dataclass
class ForecastData():
    number                      : int
    name                        : str
    startTime                   : EmpyreanDateTime
    endTime                     : EmpyreanDateTime
    isDayTime                   : bool
    temperature                 : TemperatureData()
    probabilityOfPrecipitation  : int
    wind                        : WindData()
    icon                        : str
    short                       : str
    detailed                    : list[str]

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.number = forecast_data["number"]
        self.name = forecast_data["name"]
        self.startTime = EmpyreanDateTime(from_string=forecast_data["startTime"])
        self.endTime = EmpyreanDateTime(from_string=forecast_data["endTime"])
        self.isDayTime = bool(forecast_data["isDayTime"])
        self.temperature = TemperatureData(forecast_data)
        self.probabilityOfPrecipitation = forecast_data["probabilityOfPrecipitation"]["value"]
        self.wind = WindData(forecast_data)
        self.icon = forecast_data["icon"]
        self.short = forecast_data["shortForecast"]
        detailed_with_sep = forecast_data["detailedForecast"].replace('.', './')
        self.detailed = [line for line in detailed_with_sep.split('/')]
    
    def to_json(self):
        return {
            "number"                        : self.number,
            "name"                          : self.name,
            "startTime"                     : self.startTime.as_string(),
            "endTime"                       : self.endTime.as_string(),
            "isDayTime"                     : str(self.isDayTime),
            "temperature"                   : self.temperature.value,
            "temperatureUnit"               : self.temperature.unit,
            "temperatureTrend"              : self.temperature.trend,
            "probabilityOfPrecipitation"    : {
                "unitCode"  : "wmoUnit:percent",
                "value"     : self.probabilityOfPrecipitation
            },
            "windSpeed"                     : f'{self.wind.value} {self.wind.unit}',
            "windUnit"                      : self.wind.direction,
            "icon"                          : self.icon,
            "shortForecast"                 : self.short,
            "detailedForecast"              : self.detailed
        }

@dataclass
class Elevation():
    unitCode    : str
    value       : float

@dataclass
class Forecast():
    units           : str
    generatedAt     : EmpyreanDateTime
    updateTime      : EmpyreanDateTime
    validTimes      : EmpyreanDateTime

    forecasts       : dict[EmpyreanDateTime, ForecastData]

    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.units = forecast_data["units"]
        self.generatedAt = EmpyreanDateTime(from_string=forecast_data["generatedAt"])
        self.updateTime =  EmpyreanDateTime(from_string=forecast_data["updateTime"])
        self.validTimes = EmpyreanDateTime(from_string=forecast_data["validTimes"])

        for period in forecast_data["periods"]:
            forecast = ForecastData(forecast_data["periods"][period])
            self.forecasts[forecast.startTime.as_string()] = forecast
        
    def to_json(self):
        periods = { }
        period = 0
        for dt, data in self.forecasts:
            periods[str(period)] = data.to_json()
            period += 1
        return {
            self.updateTime.as_string() : {
                "units" : self.units,
                "generatedAt" : self.generatedAt.as_string(),
                "updateTime" : self.updateTime.as_string(),
                "validTimes" : self.validTimes.as_string(),
                "periods" : periods
            }
        }