from typing import Self

from utils.structures.forecast.api.forecast import Period
from utils.structures.json.unit_value import UnitValue, Value_Type


class EmpyreanDescription():
    
    class Keys():
        short: str = "short"
        long:  str = "long"
    
    def __init__(self) -> None:
        self.short: UnitValue = None
        self.long: UnitValue  = None

    @staticmethod
    def from_API(period: Period) -> Self:
        new_instance = EmpyreanDescription()
        new_instance.short = UnitValue({
            UnitValue.Keys.unitCode : "",
            UnitValue.Keys.value    : period.shortForecast,
            UnitValue.Keys.valueType: Value_Type.STRING
        })
        new_instance.long = UnitValue({
            UnitValue.Keys.unitCode : "",
            UnitValue.Keys.value    : period.detailedForecast,
            UnitValue.Keys.valueType: Value_Type.STRING
        })
        return new_instance

    @staticmethod
    def from_Empyrean(description: dict[str, dict[str, str]]) -> Self:
        new_instance = EmpyreanDescription()
        new_instance.short = UnitValue(description[EmpyreanDescription.Keys.short])
        new_instance.long = UnitValue(description[EmpyreanDescription.Keys.long])
        return new_instance

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            EmpyreanDescription.Keys.short : self.short.to_dict(),
            EmpyreanDescription.Keys.long  : self.long.to_dict()
        }