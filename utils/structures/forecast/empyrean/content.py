"""Module for the Program's data structure implementation of forecast information"""
from typing import Any, Self

from utils.structures.forecast.api.forecast import Period
from utils.structures.forecast.empyrean.description import EmpyreanDescription
from utils.structures.forecast.empyrean.wind import Wind
from utils.structures.json.unit_value import UnitValue, ValueType


class EmpyreanForecastContent():
    """The container for organizing forecast information to be easily
    manipulated/access by the program."""
    class Keys():
        """Helper class for mapping dictionary keys to variables"""
        temperature: str = "temperature"
        rainChance: str = "rainChance"
        dewPoint: str = "dewPoint"
        relativeHumidity: str = "relativeHumidity"
        wind: str = "wind"
        description: str = "description"

    class DisplayKeys():
        """Helper class for mapping variables to display strings"""
        temperature: str = "Temperature"
        rainChance: str = "Rain Chance"
        dewPoint: str = "Dew Point"
        relativeHumidity: str = "Relative Humidity"
        wind: str = "Wind"
        description: str = "Forecast"

    def __init__(self) -> None:
        self.temperature: UnitValue             = None
        self.rainChance: UnitValue              = None
        self.dewPoint: UnitValue                = None
        self.relativeHumidity: UnitValue        = None
        self.wind: Wind                         = None
        self.description: EmpyreanDescription   = None

    @staticmethod
    def from_API(period: Period) -> Self:
        """Helper function to generate a new instance from API information."""
        new_instance = EmpyreanForecastContent()
        new_instance.temperature = UnitValue({
            UnitValue.Keys.unitCode     : period.temperatureUnit,
            UnitValue.Keys.value        : period.temperature,
            UnitValue.Keys.valueType    : ValueType.INTEGER
        })
        new_instance.rainChance = UnitValue({
            UnitValue.Keys.unitCode     : period.probabilityOfPrecipitation[UnitValue.Keys.unitCode],
            UnitValue.Keys.value        : period.probabilityOfPrecipitation[UnitValue.Keys.value],
            UnitValue.Keys.valueType    : ValueType.INTEGER
        })
        if period.dewPoint:
            new_instance.dewPoint = UnitValue({
                UnitValue.Keys.unitCode     : period.dewPoint[UnitValue.Keys.unitCode],
                UnitValue.Keys.value        : period.dewPoint[UnitValue.Keys.value],
                UnitValue.Keys.valueType    : ValueType.FLOAT
            })
        else:
            new_instance.dewPoint = UnitValue({UnitValue.Keys.unitCode: "", UnitValue.Keys.value : "", UnitValue.Keys.valueType : ValueType.STRING})
        if period.relativeHumidity:
            new_instance.relativeHumidity = UnitValue({
                UnitValue.Keys.unitCode     : period.relativeHumidity[UnitValue.Keys.unitCode],
                UnitValue.Keys.value        : period.relativeHumidity[UnitValue.Keys.value],
                UnitValue.Keys.valueType    : ValueType.INTEGER
            })
        else:
            new_instance.relativeHumidity = UnitValue({UnitValue.Keys.unitCode: "", UnitValue.Keys.value : "", UnitValue.Keys.valueType : ValueType.STRING})
        new_instance.wind = Wind.from_API(period)
        new_instance.description = EmpyreanDescription.from_API(period)
        return new_instance

    @staticmethod
    def from_Empyrean(content: dict[str, dict[str, UnitValue]]) -> Self:
        """Helper function to generate a new instance from saved JSON information"""
        new_instance = EmpyreanForecastContent()
        new_instance.temperature        = UnitValue(content[EmpyreanForecastContent.Keys.temperature])
        new_instance.rainChance         = UnitValue(content[EmpyreanForecastContent.Keys.rainChance])
        new_instance.dewPoint           = UnitValue(content[EmpyreanForecastContent.Keys.dewPoint])
        new_instance.relativeHumidity   = UnitValue(content[EmpyreanForecastContent.Keys.relativeHumidity])
        new_instance.wind               = Wind.from_Empyrean(content[EmpyreanForecastContent.Keys.wind])
        new_instance.description        = EmpyreanDescription.from_Empyrean(content[EmpyreanForecastContent.Keys.description])
        return new_instance

    def to_dict(self) -> dict[str, Any]:
        """Helper function to prepare data to be saved to JSON."""
        return {
            EmpyreanForecastContent.Keys.temperature : self.temperature.to_dict(),
            EmpyreanForecastContent.Keys.rainChance : self.rainChance.to_dict(),
            EmpyreanForecastContent.Keys.dewPoint : self.dewPoint.to_dict(),
            EmpyreanForecastContent.Keys.relativeHumidity : self.relativeHumidity.to_dict(),
            EmpyreanForecastContent.Keys.wind : self.wind.to_dict(),
            EmpyreanForecastContent.Keys.description : self.description.to_dict()
        }
