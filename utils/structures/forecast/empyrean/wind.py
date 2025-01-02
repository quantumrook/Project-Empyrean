"""Module for containing all the wind information for a time entry of a forecast."""
from typing import Self
from utils.structures.forecast.api.forecast import Period
from utils.structures.json.unit_value import UnitValue, ValueType


class Wind():
    """Contains all the wind data entry for a forecast entry."""
    class Keys():
        """Helper class for mapping keys to variables."""
        speedLow: str = "speedLow"
        speedHigh: str = "speedHigh"
        direction: str = "direction"

    def __init__(self) -> None:
        self.speedLow: UnitValue = None
        self.speedHigh: UnitValue = None
        self.direction: UnitValue = None

    @staticmethod
    def from_API(period: Period) -> Self:
        """Helper function for creation from API data."""
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
    def from_Empyrean(json_data: dict) -> Self:
        """Helper function for creation from saved JSON data."""
        new_instance = Wind()
        if Wind.Keys.speedLow in json_data.keys():
            new_instance.speedLow = UnitValue(json_data[new_instance.Keys.speedLow])

        new_instance.speedHigh = UnitValue(json_data[new_instance.Keys.speedHigh])
        new_instance.direction = UnitValue(json_data[new_instance.Keys.direction])
        return new_instance

    def get_average(self) -> UnitValue:
        """Helper function for getting the average windspeed."""
        return UnitValue({
            UnitValue.Keys.unitCode : self.speedHigh.unitCode,
            UnitValue.Keys.value : round((self.speedHigh.value + self.speedLow.value)/ 2),
            UnitValue.Keys.valueType : ValueType.INTEGER
        })

    def to_dict(self) -> dict[str, dict[str, str]]:
        """Helper function for preparing to save JSON data."""
        as_dict = {
                self.Keys.speedHigh : {
                    UnitValue.Keys.unitCode : self.speedHigh.unitCode,
                    UnitValue.Keys.value : self.speedHigh.value,
                    UnitValue.Keys.valueType : self.speedHigh.value_type.name
                },
                self.Keys.direction : {
                    UnitValue.Keys.unitCode : self.direction.unitCode,
                    UnitValue.Keys.value : self.direction.value,
                    UnitValue.Keys.valueType : self.direction.value_type.name
                }
            }
        if self.speedLow is not None:
            as_dict[self.Keys.speedLow] = {
                    UnitValue.Keys.unitCode : self.speedLow.unitCode,
                    UnitValue.Keys.value : self.speedLow.value,
                    UnitValue.Keys.valueType : self.speedLow.value_type.name
                }
        return as_dict
