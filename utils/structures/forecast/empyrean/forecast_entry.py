"""Module for wrapping a forecast."""
from typing import Any, Self

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.api.forecast import Period
from utils.structures.forecast.empyrean.content import EmpyreanForecastContent
from utils.structures.forecast.empyrean.properties import EmpyreanProperties


class EmpyreanForecastEntry():
    """Contains all the information of a forecast."""
    class Keys():
        """Helper class for mapping keys to variables."""
        class API():
            """API specific subcategory"""
            startTime: str = "startTime"
            endTime: str = "endTime"
        class Empyrean():
            """Program specific subcategory"""
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
        """Helper function for creation from API data."""
        new_instance = EmpyreanForecastEntry()
        new_instance.start = EmpyreanDateTime.from_API(period.startTime)
        new_instance.end = EmpyreanDateTime.from_API(period.endTime)
        new_instance.properties = EmpyreanProperties.from_API(period)
        new_instance.content = EmpyreanForecastContent.from_API(period)
        return new_instance

    @staticmethod
    def from_Empyrean(entry: dict[str, Any]) -> Self:
        """Helper function for creation from saved JSON data."""
        new_instance = EmpyreanForecastEntry()
        new_instance.start = EmpyreanDateTime.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.start])
        new_instance.end = EmpyreanDateTime.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.end])
        new_instance.properties = EmpyreanProperties.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.properties])
        new_instance.content = EmpyreanForecastContent.from_Empyrean(entry[EmpyreanForecastEntry.Keys.Empyrean.content])
        return new_instance

    def to_dict(self) -> dict[str, Any]:
        """Helper function for preparing to save JSON data."""
        return {
            EmpyreanForecastEntry.Keys.Empyrean.start : self.start.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.end: self.end.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.properties : self.properties.to_dict(),
            EmpyreanForecastEntry.Keys.Empyrean.content : self.content.to_dict()
        }
