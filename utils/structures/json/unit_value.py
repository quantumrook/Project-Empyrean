from dataclasses import dataclass
import re

from utils.structures.empyrean_enum import EmpyreanEnum


@dataclass
class UnitValueKeys():
    unitCode = "unitCode"
    value = "value"
    valueType = "valueType"

    def __init__(self, key) -> None:
        self.key = key

class Value_Type(EmpyreanEnum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"

@dataclass
class UnitValue():
    unitCode: str
    value: str
    value_type: Value_Type

    _allowed_error = 1e-5

    def __init__(self, unitValue: dict[str, str]) -> None:
        self.unitCode: str = unitValue["unitCode"]
        self.value: str = str(unitValue["value"])
        
        if "valueType" in list(unitValue.keys()):
            self.value_type: Value_Type = Value_Type.from_string(unitValue["valueType"])
        elif '.' in self.value:
            self.value_type: Value_Type = Value_Type.FLOAT
        elif str.isdigit(self.value):
            self.value_type: Value_Type = Value_Type.INTEGER
        else:
            self.value_type: Value_Type = Value_Type.STRING
            

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
            UnitValueKeys.value : self.get_value(),
            UnitValueKeys.valueType : self.value_type.name
        }


class JSON_EmpyreanObject():
    def __init__(self, keys: list[str]) -> None:
        self.unitvalue_keys: list[UnitValueKeys] = [ ]
        
        for key in keys:
            self.unitvalue_keys.append(UnitValueKeys(key))
        
        self.unitvalues: dict[str, UnitValue] = { }

class PossibleWindImplementation(JSON_EmpyreanObject):

    def __init__(self, wind: dict[str, UnitValue]) -> None:
        super().__init__(keys=list(wind.keys()))

        for uv_key in self.unitvalue_keys:
            self.unitvalues[uv_key.key] = UnitValue(wind[uv_key.key])

    def get_average(self) -> UnitValue:
        average, num_added = 0
        for unitvalue_key in self.unitvalue_keys:
            if Value_Type.is_numeric(unitvalue_key.valueType):
                average += self.unitvalues[unitvalue_key.key].get_value()
                num_added += 1

        return UnitValue(
            unitCode= self.unitvalues[self.unitvalue_keys[0].key].unitCode,
            value= round(average/num_added),
            value_type= Value_Type.INTEGER
        )

    def to_dict(self) -> dict[str, dict[str, str]]:
        as_dict = { }
        for uv_key in self.unitvalue_keys:
            if self.unitvalues[uv_key.key]:
                as_dict[uv_key.key] = {
                    uv_key.unitCode : self.unitvalues[uv_key.key].unitCode,
                    uv_key.value    : self.unitvalues[uv_key.key].value,
                    uv_key.valueType: self.unitvalues[uv_key.key].value_type.name
                }
        return as_dict
