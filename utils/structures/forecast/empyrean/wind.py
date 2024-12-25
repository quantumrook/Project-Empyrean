from typing import Self
from utils.structures.forecast.api.forecast import Period
from utils.structures.json.unit_value import UnitValue, Value_Type


class Wind():

    class Keys():
        speedLow: str = "speedLow"
        speedHigh: str = "speedHigh"
        direction: str = "direction"
    
    def __init__(self) -> None:
        self.speedLow: UnitValue = None
        self.speedHigh: UnitValue = None
        self.direction: UnitValue = None

    @staticmethod
    def from_API(period: Period) -> Self:
        new_instance = Wind()
        wind_split = period.windSpeed.split(' ')

        if len(wind_split) > 2:
            new_instance.speedLow = UnitValue({
                UnitValue.Keys.unitCode     : wind_split[-1], 
                UnitValue.Keys.value        : wind_split[0]
            })
            new_instance.speedHigh = UnitValue({
                UnitValue.Keys.unitCode    : wind_split[-1],
                UnitValue.Keys.value       : wind_split[2]
            })
        else:
            new_instance.speedHigh = UnitValue({
                UnitValue.Keys.unitCode    : wind_split[-1], 
                UnitValue.Keys.value       : wind_split[0]
            })

        new_instance.direction = UnitValue({
            UnitValue.Keys.unitCode    : "Cardinal", 
            UnitValue.Keys.value       : period.windDirection
        })
        return new_instance

    @staticmethod
    def from_Empyrean(json_data) -> Self:
        new_instance = Wind()
        if json_data[new_instance.Keys.speedLow]:
            new_instance.speedLow = UnitValue(json_data[new_instance.Keys.speedLow])
        
        new_instance.speedHigh = UnitValue(json_data[new_instance.Keys.speedHigh])
        new_instance.direction = UnitValue(json_data[new_instance.Keys.direction])
        return new_instance

    def get_average(self) -> UnitValue:
        return UnitValue(
            unitCode= self.speedHigh.unitCode,
            value= round((self.speedHigh.value + self.speedLow.value)/ 2),
            value_type= Value_Type.INTEGER
        )

    def to_dict(self) -> dict[str, dict[str, str]]:
        as_dict = {
                self.Keys.speedHigh.key : {
                    self.Keys.speedHigh.unitCode : self.speedHigh.unitCode,
                    self.Keys.speedHigh.value : self.speedHigh.value,
                    self.Keys.speedHigh.valueType : self.speedHigh.value_type.name
                },
                self.Keys.direction.key : {
                    self.Keys.direction.unitCode : self.direction.unitCode,
                    self.Keys.direction.value : self.direction.value,
                    self.Keys.direction.valueType : self.direction.value_type.name
                }
            }
        if self.speedLow is not None:
            as_dict[self.Keys.speedLow.key] = {
                    self.Keys.speedLow.unitCode : self.speedLow.unitCode,
                    self.Keys.speedLow.value : self.speedLow.value,
                    self.Keys.speedLow.valueType : self.speedLow.value_type.name
                }
        return as_dict

