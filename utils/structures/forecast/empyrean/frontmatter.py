from typing import Any, Self

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.api.forecast import PropertiesData
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.json.unit_value import UnitValue, Value_Type


class EmpyreanFrontmatter():

    class Keys():
        type: str = "type"
        generated: str = "generated"
        updated: str = "updated"
        expiration: str = "expiration"
        elevation: str = "elevation"

    def __init__(self) -> None:
        self.forecast_type: ForecastType = None
        self.generated: EmpyreanDateTime = None
        self.updated: EmpyreanDateTime = None
        self.expiration: EmpyreanDateTime = None
        self.elevation: UnitValue = None

    @staticmethod
    def from_API(properties_data: PropertiesData) -> Self:
        new_instance = EmpyreanFrontmatter()
        typename, _unused  = properties_data.forecastGenerator.split('Forecast')
        match typename.lower():
            case "hourly":
                forecast_type = ForecastType.HOURLY
            case _:
                forecast_type = ForecastType.EXTENDED
        new_instance.forecast_type = forecast_type

        new_instance.generated  = EmpyreanDateTime.from_API(location_timezone="UTC", generating_str=properties_data.generatedAt)
        new_instance.updated    = EmpyreanDateTime.from_API(location_timezone="UTC", generating_str=properties_data.updateTime)
        new_instance.expiration = EmpyreanDateTime.from_API(location_timezone="UTC", generating_str=properties_data.validTimes)
        
        new_instance.elevation = UnitValue({
            UnitValue.Keys.unitCode     : properties_data.elevation[UnitValue.Keys.unitCode],
            UnitValue.Keys.value        : properties_data.elevation[UnitValue.Keys.value],
            UnitValue.Keys.valueType    : Value_Type.FLOAT
        })
        return new_instance

    @staticmethod
    def from_Empyrean(frontmatter_data: dict[str, Any]) -> Self:
        new_instance = EmpyreanFrontmatter()
        new_instance.forecast_type  = ForecastType.from_string(frontmatter_data[EmpyreanFrontmatter.Keys.type])
        new_instance.generated      = EmpyreanDateTime.from_Empyrean(frontmatter_data[EmpyreanFrontmatter.Keys.generated])
        new_instance.updated        = EmpyreanDateTime.from_Empyrean(frontmatter_data[EmpyreanFrontmatter.Keys.updated])
        new_instance.expiration     = EmpyreanDateTime.from_Empyrean(frontmatter_data[EmpyreanFrontmatter.Keys.expiration])
        new_instance.elevation      = UnitValue(frontmatter_data[EmpyreanFrontmatter.Keys.elevation])
        return new_instance

    def to_dict(self) -> dict[str, Any]:
        return {
            EmpyreanFrontmatter.Keys.type : self.forecast_type.name,
            EmpyreanFrontmatter.Keys.generated : self.generated.to_dict(),
            EmpyreanFrontmatter.Keys.updated : self.updated.to_dict(),
            EmpyreanFrontmatter.Keys.expiration : self.expiration.to_dict(),
            EmpyreanFrontmatter.Keys.elevation : self.elevation.to_dict()
        }