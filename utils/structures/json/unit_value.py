from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class UnitValueKeys():
    unitCode = "unitCode"
    value = "value"
    valueType = "valueType"

    def __init__(self, key) -> None:
        self.key = key

class Value_Type(Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"

    @classmethod
    def list(cls) -> list:
        """
        Returns all of the widget types as a list.

        Source: https://stackoverflow.com/a/54919285
        """
        return list(map(lambda c: c.value, cls))

    @classmethod
    def from_string(cls, value_type):
        for type in cls.list():
            if type.name == value_type:
                return type
        raise ValueError(f"Tried to convert {value_type=} to Value_Type.")

@dataclass
class UnitValue():
    unitCode: str
    value: str
    value_type: Value_Type

    def __init__(self, unitValue: dict[str, str]) -> None:
        self.unitCode: str = unitValue["unitCode"]
        self.value: str = unitValue["value"]
        self.value_type: Value_Type = Value_Type.from_string(unitValue["valueType"])

    def get_unit(self):
        unitCode, unit = self.unitCode.split(':')
        match unit:
            case "percent":
                unit = "%"
            case "degC":
                unit = "C"
        return unit

    def get_value(self):
        match self.value_type:
            case Value_Type.INTEGER:
                return int(self.value)
            case Value_Type.FLOAT:
                return float(self.value)
            case _:
                return self.value

    def to_dict(self) -> dict[str, str]:
        return {
            UnitValueKeys.unitCode : self.unitCode,
            UnitValueKeys.value : str(self.value),
            UnitValueKeys.valueType : self.value_type.name
        }

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