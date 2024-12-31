"""Helper module for creating the base object for storing 
and retreiving JSON data into the system.
"""
from dataclasses import dataclass

from utils.structures.empyrean_enum import EmpyreanEnum


class ValueType(EmpyreanEnum):
    """Helper Enum for specifying the data type that
    should be returned when accessing the value.
    """
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"

@dataclass
class UnitValue():
    """Models the most common form of storage between the
    API and Empyrean.
    """
    unitCode: str
    value: str
    value_type: ValueType

    _allowed_error = 1e-5

    class Keys():
        """Helper class to map dictionary keys to values"""
        unitCode = "unitCode"
        value = "value"
        valueType = "valueType"

    def __init__(self, unitValue: dict[str, str]) -> None:
        self.unitCode: str = unitValue["unitCode"]
        self.value: str = str(unitValue["value"])

        if "valueType" in list(unitValue.keys()):
            self.value_type: ValueType = ValueType.from_string(unitValue["valueType"])
        elif '.' in self.value:
            self.value_type: ValueType = ValueType.FLOAT
        elif str.isdigit(self.value):
            self.value_type: ValueType = ValueType.INTEGER
        else:
            self.value_type: ValueType = ValueType.STRING

    def get_unit(self):
        """Returns the unit in a display ready format
        after stripping the wmoUnit parameter.
        """
        if self.unitCode == "F":
            return self.unitCode
        unitCode, _, unit = self.unitCode.partition(':')
        match unit:
            case "percent":
                unit = "%"
            case "degC":
                unit = "C"
        return unit

    def get_value(self):
        """Returns the value as the type it is supposed to be.
        """
        match self.value_type:
            case ValueType.INTEGER:
                if self.value != "None":
                    return int(self.value)
                else:
                    return 0
            case ValueType.FLOAT:
                if self.value != "None":
                    return float(self.value)
                else:
                    return 0
            case _:
                return self.value

    def to_dict(self) -> dict[str, str]:
        """Helper function for when converting to JSON friendly format."""
        return {
            UnitValue.Keys.unitCode : self.unitCode,
            UnitValue.Keys.value : self.get_value(),
            UnitValue.Keys.valueType : self.value_type.name
        }
