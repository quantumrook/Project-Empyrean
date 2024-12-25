from typing import Any, Self

from utils.structures.forecast.api.forecast import PropertiesData
from utils.structures.forecast.empyrean.forecast_entry import EmpyreanForecastEntry
from utils.structures.forecast.empyrean.frontmatter import EmpyreanFrontmatter


class EmpyreanForecast():

    class Keys():
        frontmatter: str = "frontmatter"
        forecasts: str = "forecasts"

    def __init__(self) -> None:
        self.frontmatter: EmpyreanFrontmatter = None
        self.forecasts: list[EmpyreanForecastEntry] = [ ]

    @staticmethod
    def from_API(properties_data: PropertiesData) -> Self:
        new_instance = EmpyreanForecast()
        new_instance.frontmatter = EmpyreanFrontmatter.from_API(properties_data)
        for entry in properties_data.periods:
            new_instance.forecasts.append(EmpyreanForecastEntry.from_API(entry, properties_data))
        return new_instance
    
    @staticmethod
    def from_Empyrean(json_data: dict[str, Any]) -> None:
        new_instance = EmpyreanForecast()
        new_instance.frontmatter = EmpyreanFrontmatter.from_Empyrean(json_data[EmpyreanForecast.Keys.frontmatter])
        for entry in json_data[EmpyreanForecast.Keys.forecasts]:
            new_instance.forecasts.append(EmpyreanForecastEntry.from_Empyrean(entry))

    def to_dict(self) -> dict[str, Any]:
        forecast_list = [ ]
        for forecast_entry in self.forecasts:
            forecast_list.append(forecast_entry.to_dict())
        return {
            EmpyreanForecast.Keys.frontmatter : self.frontmatter.to_dict(),
            EmpyreanForecast.Keys.forecasts : forecast_list
        }
    

