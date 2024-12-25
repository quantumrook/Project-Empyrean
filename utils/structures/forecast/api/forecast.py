from dataclasses import dataclass
from typing import Any


from utils.structures.json.unit_value import UnitValue, UnitValueKeys


@dataclass
class PeriodKeys():
    number = "number"
    name = "name"
    startTime = "startTime"
    endTime = "endTime"
    isDaytime = "isDaytime"
    temperature = "temperature"
    temperatureUnit = "temperatureUnit"
    temperatureTrend = "temperatureTrend"
    probabilityOfPrecipitation = UnitValueKeys("probabilityOfPrecipitation")
    dewPoint = UnitValueKeys("dewpoint")
    relativeHumidity = UnitValueKeys("relativeHumidity")
    windSpeed = "windSpeed"
    windDirection = "windDirection"
    icon = "icon"
    shortForecast = "shortForecast"
    detailedForecast = "detailedForecast"

@dataclass
class PropertiesKeys():
    units = "units"
    forecastGenerator = "forecastGenerator"
    generatedAt = "generatedAt"
    updateTime = "updateTime"
    validTimes = "validTimes"
    elevation = UnitValueKeys("elevation")
    periods = "periods"

class Period():
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int
    temperatureUnit: str
    temperatureTrend: str
    probabilityOfPrecipitation: UnitValue
    dewPoint: UnitValue
    relativeHumidity: UnitValue
    windSpeed: str
    windDirection: str
    icon: str
    shortForecast: str
    detailedForecast: str

    def __init__(self, period_data: dict[str, Any]) -> None:
        self.number = int(period_data[PeriodKeys.number])
        self.name = period_data[PeriodKeys.name]
        self.startTime = period_data[PeriodKeys.startTime]
        self.endTime = period_data[PeriodKeys.endTime]
        self.isDaytime = bool(period_data[PeriodKeys.isDaytime])
        self.temperature = int(period_data[PeriodKeys.temperature])
        self.temperatureUnit = period_data[PeriodKeys.temperatureUnit]
        self.temperatureTrend = period_data[PeriodKeys.temperatureTrend]
        self.probabilityOfPrecipitation = UnitValue(period_data[PeriodKeys.probabilityOfPrecipitation.key])
        self.dewPoint = UnitValue(period_data[PeriodKeys.dewPoint.key])
        self.relativeHumidity = UnitValue(period_data[PeriodKeys.relativeHumidity.key])
        self.windSpeed = period_data[PeriodKeys.windSpeed]
        self.windDirection = period_data[PeriodKeys.windDirection]
        self.icon = period_data[PeriodKeys.icon]
        self.shortForecast = period_data[PeriodKeys.shortForecast]
        self.detailedForecast = period_data[PeriodKeys.detailedForecast]

    def to_dict(self) -> dict[str, Any]:
        return {
            PeriodKeys.number : self.number,
            PeriodKeys.name : self.name,
            PeriodKeys.startTime : self.startTime,
            PeriodKeys.endTime : self.endTime,
            PeriodKeys.isDaytime : self.isDaytime,
            PeriodKeys.temperature : self.temperature,
            PeriodKeys.temperatureUnit : self.temperatureUnit,
            PeriodKeys.temperatureTrend : self.temperatureTrend,
            PeriodKeys.probabilityOfPrecipitation.key : self.probabilityOfPrecipitation.to_dict(),
            PeriodKeys.dewPoint.key : self.dewPoint.to_dict(),
            PeriodKeys.relativeHumidity.key : self.relativeHumidity.to_dict(),
            PeriodKeys.windSpeed : self.windSpeed,
            PeriodKeys.windDirection : self.windDirection,
            PeriodKeys.icon : self.icon,
            PeriodKeys.shortForecast : self.shortForecast,
            PeriodKeys.detailedForecast : self.detailedForecast
        }

@dataclass
class PropertiesData():
    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: UnitValue
    periods: list[ Period]

    def __init__(self, properties_data: dict[str, Any]) -> None:
        self.units = properties_data[PropertiesKeys.units]
        self.forecastGenerator = properties_data[PropertiesKeys.forecastGenerator]
        self.generatedAt = properties_data[PropertiesKeys.generatedAt]
        self.updateTime = properties_data[PropertiesKeys.updateTime]
        self.validTimes = properties_data[PropertiesKeys.validTimes]
        self.elevation = UnitValue(properties_data[PropertiesKeys.elevation.key])
        self.periods = [ ]
        for p in properties_data[PropertiesKeys.periods]:
            self.periods.append(Period(p))

    def to_dict(self) -> dict[str, Any]:
        periods_in_list = [ ]
        for p in self.periods:
            periods_in_list.append(p.to_dict())
        return {
            PropertiesKeys.units: self.units,
            PropertiesKeys.forecastGenerator: self.forecastGenerator,
            PropertiesKeys.generatedAt: self.generatedAt,
            PropertiesKeys.updateTime: self.updateTime,
            PropertiesKeys.validTimes: self.validTimes,
            PropertiesKeys.elevation.key: self.elevation.to_dict(),
            PropertiesKeys.periods : periods_in_list
        }
