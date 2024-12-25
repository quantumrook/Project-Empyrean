from dataclasses import dataclass
from typing import Any


from utils.structures.datetime import EmpyreanDateTime
from utils.structures.json.unit_value import UnitValue, UnitValueKeys, Value_Type
from utils.structures.forecast.forecast_type import ForecastType

@dataclass
class JSON_Datetime():
    def __init__(self, datetime: dict[str, str]) -> None:
        self.date: str = datetime["date"]
        self.time: str = datetime["time"]
        self.time_zone: str = datetime["time_zone"]

    def to_EmpyreanDateTime(self) -> EmpyreanDateTime:
        return EmpyreanDateTime(location_timezone=self.time_zone, generating_str=f"{self.date} {self.time}")


class Wind():

    def __init__(self, wind: dict[str, UnitValue]) -> None:
        self.speedLowKeys: UnitValueKeys = UnitValueKeys("speedLow")
        self.speedHighKeys: UnitValueKeys = UnitValueKeys("speedHigh")
        self.directionKeys: UnitValueKeys = UnitValueKeys("direction")

        if wind[self.speedLowKeys.key]:
            self.speedLow: UnitValue = UnitValue(wind[self.speedLowKeys.key])
        
        self.speedHigh: UnitValue = UnitValue(wind[self.speedHighKeys.key])
        self.direction: UnitValue = UnitValue(wind[self.directionKeys.key])

    def get_average(self) -> UnitValue:
        return UnitValue(
            unitCode= self.speedHigh.unitCode,
            value= round((self.speedHigh.value + self.speedLow.value)/ 2),
            value_type= Value_Type.INTEGER
        )

    def to_dict(self) -> dict[str, dict[str, str]]:
        as_dict = {
                self.speedHighKeys.key : {
                    self.speedHighKeys.unitCode : self.speedHigh.unitCode,
                    self.speedHighKeys.value : self.speedHigh.value,
                    self.speedHighKeys.valueType : self.speedHigh.value_type.name
                },
                self.directionKeys.key : {
                    self.directionKeys.unitCode : self.direction.unitCode,
                    self.directionKeys.value : self.direction.value,
                    self.directionKeys.valueType : self.direction.value_type.name
                }
            }
        if self.speedLow is not None:
            as_dict[self.speedLowKeys.key] = {
                    self.speedLowKeys.unitCode : self.speedLow.unitCode,
                    self.speedLowKeys.value : self.speedLow.value,
                    self.speedLowKeys.valueType : self.speedLow.value_type.name
                }
        return as_dict

@dataclass
class EmpyreanFrontMatterKeys():
    key: str = "frontmatter"
    type: str = "type"
    generated: str = "generated"
    updated: str = "updated"
    expiration: str = "expiration"
    elevation: str = "elevation"

class EmpyreanFrontmatter():
    def __init__(self, frontmatter: dict[str, Any]) -> None:
        self.forecast_type: ForecastType = ForecastType.from_string(frontmatter[EmpyreanFrontMatterKeys.type])

        self.generated: EmpyreanDateTime = JSON_Datetime(frontmatter[EmpyreanFrontMatterKeys.generated]).to_EmpyreanDateTime()
        self.updated: EmpyreanDateTime = JSON_Datetime(frontmatter[EmpyreanFrontMatterKeys.updated]).to_EmpyreanDateTime()
        self.expiration: EmpyreanDateTime = JSON_Datetime(frontmatter[EmpyreanFrontMatterKeys.expiration]).to_EmpyreanDateTime()

        self.elevation: UnitValue = UnitValue(frontmatter[EmpyreanFrontMatterKeys.elevation])

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanFrontMatterKeys.type : self.forecast_type.name,
            EmpyreanFrontMatterKeys.generated : self.generated.to_dict(),
            EmpyreanFrontMatterKeys.updated : self.updated.to_dict(),
            EmpyreanFrontMatterKeys.expiration : self.expiration.to_dict(),
            EmpyreanFrontMatterKeys.elevation : self.elevation.to_dict()
        }

@dataclass
class EmpyreanPropertiesKeys():
    name: str = "name"
    isDaytime: str = "isDaytime"
    icon: str = "icon"


class EmpyreanProperties():
    def __init__(self, properties: dict[str, Any]) -> None:
        self.name: str = properties["name"]
        self.isDaytime: bool = bool(properties["isDaytime"])
        self.icon: str = properties["icon"]
    
    def to_dict(self) -> dict[str, str]:
        return {
            EmpyreanPropertiesKeys.name : self.name,
            EmpyreanPropertiesKeys.isDaytime : str(self.isDaytime),
            EmpyreanPropertiesKeys.icon : self.icon
        }

@dataclass
class EmpyreanDescriptionKeys():
    short: str = "short"
    long: str = "long"

class EmpyreanDescription():
    def __init__(self, description: dict[str, dict[str, str]]) -> None:
        self.short: UnitValue = UnitValue(description[EmpyreanDescriptionKeys.short])
        self.long: UnitValue = UnitValue(description[EmpyreanDescriptionKeys.long])

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            EmpyreanDescriptionKeys.short : self.short.to_dict(),
            EmpyreanDescriptionKeys.long : self.long.to_dict()
        }

@dataclass
class EmpyreanForecastContentKeys():
    temperature: str = "temperature"
    rainChance: str = "rainChance"
    dewPoint: str = "dewPoint"
    relativeHumidity: str = "relativeHumidity"
    wind: str = "wind"
    description: str = "description"

class EmpyreanForecastContent():
    def __init__(self, content: dict[str, dict[str, UnitValue]]) -> None:
        self.temperature: UnitValue = content[EmpyreanForecastContentKeys.temperature]
        self.rainChance: UnitValue = content[EmpyreanForecastContentKeys.rainChance]
        self.dewPoint: UnitValue = content[EmpyreanForecastContentKeys.dewPoint]
        self.relativeHumidity: UnitValue = content[EmpyreanForecastContentKeys.relativeHumidity]
        self.wind: Wind = Wind(content[EmpyreanForecastContentKeys.wind])
        self.description: EmpyreanDescription = EmpyreanDescription(content[EmpyreanForecastContentKeys.description])

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanForecastContentKeys.temperature : self.temperature.to_dict(),
            EmpyreanForecastContentKeys.rainChance : self.rainChance.to_dict(),
            EmpyreanForecastContentKeys.dewPoint : self.dewPoint.to_dict(),
            EmpyreanForecastContentKeys.relativeHumidity : self.relativeHumidity.to_dict(),
            EmpyreanForecastContentKeys.wind : self.wind.to_dict(),
            EmpyreanForecastContentKeys.description : self.description.to_dict()
        }

@dataclass
class EmpyreanForecastEntryKeys():
    start: str = "start"
    end: str = "end"
    properties: str = "properties"
    content: str = "content"

class EmpyreanForecastEntry():
    def __init__(self, entry: dict[str, Any]) -> None:
        self.start: EmpyreanDateTime = JSON_Datetime(entry["start"]).to_EmpyreanDateTime()
        self.end: EmpyreanDateTime = JSON_Datetime(entry["end"]).to_EmpyreanDateTime()
        self.properties: EmpyreanProperties = EmpyreanProperties(entry["properties"])
        self.content: EmpyreanForecastContent = EmpyreanForecastContent(entry["content"])

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanForecastEntryKeys.start : self.start.to_dict(),
            EmpyreanForecastEntryKeys.end: self.end.to_dict(),
            EmpyreanForecastEntryKeys.properties : self.properties.to_dict(),
            EmpyreanForecastEntryKeys.content : self.content.to_dict()
        }

@dataclass
class EmpyreanForecastKeys():
    frontmatter: str = "frontmatter"
    forecasts: str = "forecasts"

class EmpyreanForecast():

    def __init__(self, json_data: dict[str, Any]) -> None:
        self.frontmatter: EmpyreanFrontmatter = EmpyreanFrontmatter(json_data[EmpyreanForecastKeys.frontmatter])
        self.forecasts: list[EmpyreanForecastEntry] = [ ]
        for entry in json_data[EmpyreanForecastKeys.forecasts]:
            self.forecasts.append(EmpyreanForecastEntry(entry))

    def to_dict(self) -> dict[str, Any]:
        forecast_list = [ ]
        for forecast_entry in self.forecasts:
            forecast_list.append(forecast_entry.to_dict())
        return {
            EmpyreanForecastKeys.frontmatter : self.frontmatter.to_dict(),
            EmpyreanForecastKeys.forecasts : forecast_list
        }