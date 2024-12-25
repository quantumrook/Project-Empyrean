from typing import Any

from utils.structures.json.unit_value import UnitValue


class Period():
    class Keys():
        number = "number"
        name = "name"
        startTime = "startTime"
        endTime = "endTime"
        isDaytime = "isDaytime"
        temperature = "temperature"
        temperatureUnit = "temperatureUnit"
        temperatureTrend = "temperatureTrend"
        probabilityOfPrecipitation = "probabilityOfPrecipitation"
        dewPoint = "dewpoint"
        relativeHumidity = "relativeHumidity"
        windSpeed = "windSpeed"
        windDirection = "windDirection"
        icon = "icon"
        shortForecast = "shortForecast"
        detailedForecast = "detailedForecast"
    
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int
    temperatureUnit: str
    temperatureTrend: str
    probabilityOfPrecipitation: dict[str, Any]
    dewPoint: dict[str, Any]
    relativeHumidity: dict[str, Any]
    windSpeed: str
    windDirection: str
    icon: str
    shortForecast: str
    detailedForecast: str

    def __init__(self, period_data: dict[str, Any]) -> None:
        self.number = int(period_data[Period.Keys.number])
        self.name = period_data[Period.Keys.name]
        self.startTime = period_data[Period.Keys.startTime]
        self.endTime = period_data[Period.Keys.endTime]
        self.isDaytime = bool(period_data[Period.Keys.isDaytime])
        self.temperature = int(period_data[Period.Keys.temperature])
        self.temperatureUnit = period_data[Period.Keys.temperatureUnit]
        self.temperatureTrend = period_data[Period.Keys.temperatureTrend]
        self.probabilityOfPrecipitation = period_data[Period.Keys.probabilityOfPrecipitation]
        self.dewPoint = period_data[Period.Keys.dewPoint]
        self.relativeHumidity = period_data[Period.Keys.relativeHumidity]
        self.windSpeed = period_data[Period.Keys.windSpeed]
        self.windDirection = period_data[Period.Keys.windDirection]
        self.icon = period_data[Period.Keys.icon]
        self.shortForecast = period_data[Period.Keys.shortForecast]
        self.detailedForecast = period_data[Period.Keys.detailedForecast]

    def to_dict(self) -> dict[str, Any]:
        return {
            Period.Keys.number : self.number,
            Period.Keys.name : self.name,
            Period.Keys.startTime : self.startTime,
            Period.Keys.endTime : self.endTime,
            Period.Keys.isDaytime : self.isDaytime,
            Period.Keys.temperature : self.temperature,
            Period.Keys.temperatureUnit : self.temperatureUnit,
            Period.Keys.temperatureTrend : self.temperatureTrend,
            Period.Keys.probabilityOfPrecipitation.key : self.probabilityOfPrecipitation.to_dict(),
            Period.Keys.dewPoint.key : self.dewPoint.to_dict(),
            Period.Keys.relativeHumidity.key : self.relativeHumidity.to_dict(),
            Period.Keys.windSpeed : self.windSpeed,
            Period.Keys.windDirection : self.windDirection,
            Period.Keys.icon : self.icon,
            Period.Keys.shortForecast : self.shortForecast,
            Period.Keys.detailedForecast : self.detailedForecast
        }


class PropertiesData():
    class Keys():
        units = "units"
        forecastGenerator = "forecastGenerator"
        generatedAt = "generatedAt"
        updateTime = "updateTime"
        validTimes = "validTimes"
        elevation = "elevation"
        periods = "periods"
    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: UnitValue
    periods: list[ Period]

    def __init__(self, properties_data: dict[str, Any]) -> None:
        self.units = properties_data[PropertiesData.Keys.units]
        self.forecastGenerator = properties_data[PropertiesData.Keys.forecastGenerator]
        self.generatedAt = properties_data[PropertiesData.Keys.generatedAt]
        self.updateTime = properties_data[PropertiesData.Keys.updateTime]
        self.validTimes = properties_data[PropertiesData.Keys.validTimes]
        self.elevation = properties_data[PropertiesData.Keys.elevation]
        self.periods = [ ]
        for p in properties_data[PropertiesData.Keys.periods]:
            self.periods.append(Period(p))

    def to_dict(self) -> dict[str, Any]:
        periods_in_list = [ ]
        for p in self.periods:
            periods_in_list.append(p.to_dict())
        return {
            PropertiesData.Keys.units: self.units,
            PropertiesData.Keys.forecastGenerator: self.forecastGenerator,
            PropertiesData.Keys.generatedAt: self.generatedAt,
            PropertiesData.Keys.updateTime: self.updateTime,
            PropertiesData.Keys.validTimes: self.validTimes,
            PropertiesData.Keys.elevation.key: self.elevation.to_dict(),
            PropertiesData.Keys.periods : periods_in_list
        }