from dataclasses import dataclass

from utils.structures.empyrean_enum import EmpyreanEnum


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

    class Keys():
        unitCode = "unitCode"
        value = "value"
        valueType = "valueType"

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
        match self.value_type:
            case Value_Type.INTEGER:
                if self.value != "None":
                    return int(self.value)
                else:
                    return 0
            case Value_Type.FLOAT:
                if self.value != "None":
                    return float(self.value)
                else:
                    return 0
            case _:
                return self.value

    def to_dict(self) -> dict[str, str]:
        return {
            UnitValue.Keys.unitCode : self.unitCode,
            UnitValue.Keys.value : self.get_value(),
            UnitValue.Keys.valueType : self.value_type.name
        }