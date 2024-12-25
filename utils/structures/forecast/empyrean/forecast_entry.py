from typing import Any, Self

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.api.forecast import Period
from utils.structures.forecast.empyrean.content import EmpyreanForecastContent
from utils.structures.forecast.empyrean.properties import EmpyreanProperties


class EmpyreanForecastEntry():
    class Keys():
        class API():
            startTime: str = "startTime"
            endTime: str = "endTime"
        class Empyrean():
            start: str = "start"
            end: str = "end"
            properties: str = "properties"
            content: str = "content"
    
    def __init__(self) -> None:
        self.start: EmpyreanDateTime = None
        self.end: EmpyreanDateTime = None
        self.properties: EmpyreanProperties = None
        self.content: EmpyreanForecastContent = None

    @staticmethod
    def from_API(period: Period) -> Self:
        new_instance = EmpyreanForecastEntry()
        new_instance.start = EmpyreanDateTime.from_API(period.startTime)
        new_instance.end = EmpyreanDateTime.from_API(period.endTime)
        new_instance.properties = EmpyreanProperties.from_API(period)
        new_instance.content = EmpyreanForecastContent.from_API(period)

    @staticmethod
    def from_Empyrean(entry: dict[str, Any]) -> Self:
        new_instance = EmpyreanForecastEntry()
        new_instance.start = EmpyreanDateTime.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.start])
        new_instance.end = EmpyreanDateTime.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.end])
        new_instance.properties = EmpyreanProperties.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.properties])
        new_instance.content = EmpyreanForecastContent.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.content])
        return new_instance

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanForecastEntry.Keys.Empyrean.start : self.start.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.end: self.end.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.properties : self.properties.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.content : self.content.to_dict()
        }