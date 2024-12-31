"""Module for wrapping the forecast description."""
from typing import Self

from utils.structures.forecast.api.forecast import Period
from utils.structures.json.unit_value import UnitValue, ValueType


class EmpyreanDescription():
    """Contains the short and detailed description of a forecast."""
    class Keys():
        """Helper class for mapping keys to variables."""
        short: str = "short"
        long:  str = "long"

    def __init__(self) -> None:
        self.short: UnitValue = None
        self.long: UnitValue  = None

    @staticmethod
    def from_API(period: Period) -> Self:
        """Helper function for creation from API data."""
        new_instance = EmpyreanDescription()
        new_instance.short = UnitValue({
            UnitValue.Keys.unitCode : "",
            UnitValue.Keys.value    : period.shortForecast,
            UnitValue.Keys.valueType: ValueType.STRING
        })
        new_instance.long = UnitValue({
            UnitValue.Keys.unitCode : "",
            UnitValue.Keys.value    : period.detailedForecast,
            UnitValue.Keys.valueType: ValueType.STRING
        })
        return new_instance

    @staticmethod
    def from_Empyrean(description: dict[str, dict[str, str]]) -> Self:
        """Helper function for creation from saved JSON data."""
        new_instance = EmpyreanDescription()
        new_instance.short = UnitValue(description[EmpyreanDescription.Keys.short])
        new_instance.long = UnitValue(description[EmpyreanDescription.Keys.long])
        return new_instance

    def to_dict(self) -> dict[str, dict[str, str]]:
        """Helper function for preparing to save JSON data."""
        return {
            EmpyreanDescription.Keys.short : self.short.to_dict(),
            EmpyreanDescription.Keys.long  : self.long.to_dict()
        }
