from typing import Any, Self

from utils.structures.forecast.api.forecast import Period
from utils.structures.forecast.empyrean.description import EmpyreanDescription
from utils.structures.forecast.empyrean.wind import Wind
from utils.structures.json.unit_value import UnitValue, Value_Type


class EmpyreanForecastContent():

    class Keys():
        temperature: str = "temperature"
        rainChance: str = "rainChance"
        dewPoint: str = "dewPoint"
        relativeHumidity: str = "relativeHumidity"
        wind: str = "wind"
        description: str = "description"

    class DisplayKeys():
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
        new_instance = EmpyreanForecastContent()
        new_instance.temperature = UnitValue({
            UnitValue.Keys.unitCode     : period.temperatureUnit,
            UnitValue.Keys.value        : period.temperature,
            UnitValue.Keys.valueType    : Value_Type.INTEGER
        })
        new_instance.rainChance = UnitValue({
            UnitValue.Keys.unitCode     : period.probabilityOfPrecipitation[UnitValue.Keys.unitCode],
            UnitValue.Keys.value        : period.probabilityOfPrecipitation[UnitValue.Keys.value],
            UnitValue.Keys.valueType    : Value_Type.INTEGER
        })
        if period.dewPoint:
            new_instance.dewPoint = UnitValue({
                UnitValue.Keys.unitCode     : period.dewPoint[UnitValue.Keys.unitCode],
                UnitValue.Keys.value        : period.dewPoint[UnitValue.Keys.value],
                UnitValue.Keys.valueType    : Value_Type.FLOAT
            })
        else:
            new_instance.dewPoint = UnitValue({UnitValue.Keys.unitCode: "", UnitValue.Keys.value : "", UnitValue.Keys.valueType : Value_Type.STRING})
        if period.relativeHumidity:
            new_instance.relativeHumidity = UnitValue({
                UnitValue.Keys.unitCode     : period.relativeHumidity[UnitValue.Keys.unitCode],
                UnitValue.Keys.value        : period.relativeHumidity[UnitValue.Keys.value],
                UnitValue.Keys.valueType    : Value_Type.INTEGER
            })
        else:
            new_instance.relativeHumidity = UnitValue({UnitValue.Keys.unitCode: "", UnitValue.Keys.value : "", UnitValue.Keys.valueType : Value_Type.STRING})
        new_instance.wind = Wind.from_API(period)
        new_instance.description = EmpyreanDescription.from_API(period)
        return new_instance

    @staticmethod
    def from_Empyrean(content: dict[str, dict[str, UnitValue]]) -> Self:
        new_instance = EmpyreanForecastContent()
        new_instance.temperature        = UnitValue(content[EmpyreanForecastContent.Keys.temperature])
        new_instance.rainChance         = UnitValue(content[EmpyreanForecastContent.Keys.rainChance])
        new_instance.dewPoint           = UnitValue(content[EmpyreanForecastContent.Keys.dewPoint])
        new_instance.relativeHumidity   = UnitValue(content[EmpyreanForecastContent.Keys.relativeHumidity])
        new_instance.wind               = Wind.from_Empyrean(content[EmpyreanForecastContent.Keys.wind])
        new_instance.description        = EmpyreanDescription.from_Empyrean(content[EmpyreanForecastContent.Keys.description])
        return new_instance

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanForecastContent.Keys.temperature : self.temperature.to_dict(),
            EmpyreanForecastContent.Keys.rainChance : self.rainChance.to_dict(),
            EmpyreanForecastContent.Keys.dewPoint : self.dewPoint.to_dict(),
            EmpyreanForecastContent.Keys.relativeHumidity : self.relativeHumidity.to_dict(),
            EmpyreanForecastContent.Keys.wind : self.wind.to_dict(),
            EmpyreanForecastContent.Keys.description : self.description.to_dict()
        }