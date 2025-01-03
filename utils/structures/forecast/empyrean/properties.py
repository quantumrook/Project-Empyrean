"""Module for wrapping the forecast's property information."""
from typing import Any, Self

from utils.structures.forecast.api.forecast import Period


class EmpyreanProperties():
    """Wraps useful properties of a forecast for easy accessibilty."""
    class Keys():
        """Helper class for mapping keys to variables."""
        name: str       = "name"
        isDaytime: str  = "isDaytime"
        icon: str       = "icon"

    def __init__(self) -> None:
        self.name: str = ""
        self.isDaytime: bool = False
        self.icon: str = ""

    @staticmethod
    def from_API(period: Period) -> Self:
        """Helper function for creation from API data."""
        new_instance = EmpyreanProperties()
        new_instance.name = period.name
        new_instance.isDaytime = bool(period.isDaytime)
        new_instance.icon = period.icon #TODO :: Convert API link of icon to local path
        return new_instance

    @staticmethod
    def from_Empyrean(properties: dict[str, Any]) -> Self:
        """Helper function for creation from saved JSON data."""
        new_instance = EmpyreanProperties()
        new_instance.name = properties[EmpyreanProperties.Keys.name]
        new_instance.isDaytime = bool(properties[EmpyreanProperties.Keys.isDaytime])
        new_instance.icon = properties[EmpyreanProperties.Keys.icon]
        return new_instance

    def to_dict(self) -> dict[str, str]:
        """Helper function for preparing to save JSON data."""
        return {
            EmpyreanProperties.Keys.name : self.name,
            EmpyreanProperties.Keys.isDaytime : str(self.isDaytime),
            EmpyreanProperties.Keys.icon : self.icon
        }
