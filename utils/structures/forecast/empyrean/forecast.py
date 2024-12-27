from dataclasses import dataclass
from typing import Any, Self

from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.api.forecast import PropertiesData
from utils.structures.forecast.empyrean.content import EmpyreanForecastContent
from utils.structures.forecast.empyrean.forecast_entry import EmpyreanForecastEntry
from utils.structures.forecast.empyrean.frontmatter import EmpyreanFrontmatter
from utils.text_wrapper import format_text_as_wrapped


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
            new_instance.forecasts.append(EmpyreanForecastEntry.from_API(entry))
        return new_instance
    
    @staticmethod
    def from_Empyrean(json_data: dict[str, Any]) -> Self:
        new_instance = EmpyreanForecast()
        new_instance.frontmatter = EmpyreanFrontmatter.from_Empyrean(json_data[EmpyreanForecast.Keys.frontmatter])
        for entry in json_data[EmpyreanForecast.Keys.forecasts]:
            new_instance.forecasts.append(EmpyreanForecastEntry.from_Empyrean(entry))
        return new_instance
    
    def to_dict(self) -> dict[str, Any]:
        forecast_list = [ ]
        for forecast_entry in self.forecasts:
            forecast_list.append(forecast_entry.to_dict())
        return {
            EmpyreanForecast.Keys.frontmatter : self.frontmatter.to_dict(),
            EmpyreanForecast.Keys.forecasts : forecast_list
        }
    
    def get_forecast_for_range(self, starting_datetime: EmpyreanDateTime, ending_datetime: EmpyreanDateTime) -> list[dict[EmpyreanDateTime, EmpyreanForecastContent]]:
        forecast_for_range = [ ]
        for entry in self.forecasts:
            if EmpyreanDateTime.is_in_range(entry.start, starting_datetime, ending_datetime):
                forecast_for_range.append({entry.start : entry.content})
        return forecast_for_range

    def to_hourly_tree_dict(self) -> list[dict[str, Any]]:
        now = EmpyreanDateTime.now()
        date_entry = None
        for entry in self.forecasts:
            if entry.start.date == now.date and entry.start.hour() >= now.hour():
                open_flag = True
                if date_entry is None:
                    date_entry = TreeEntry(name=entry.start.date, is_open=open_flag, subdata=[ ])

                entry_subdata = [
                    TreeEntry(name=entry.content.Keys.temperature, is_open=True, value=f"{entry.content.temperature.get_value()} {entry.content.temperature.get_unit()}"),
                    TreeEntry(name=entry.content.Keys.rainChance, is_open=True, value=f"{entry.content.rainChance.get_value()} {entry.content.rainChance.get_unit()}")
                ]

                tree_entry = TreeEntry(name=entry.start.time, is_open=open_flag, subdata=entry_subdata)
                date_entry.subdata.append(tree_entry)
        return [ date_entry.to_dict() ]
    
    def to_extended_tree_dict(self) -> list[dict[str, Any]]: 
        entries = [ ]
        today = EmpyreanDateTime.now().date
        new_date = True
        date_entry = None
        for entry in self.forecasts:
            if entry.start.date == today:
                open_flag = True
            else:
                open_flag = False

            if date_entry is not None and entry.start.date != date_entry.name:
                new_date = True
                entries.append(date_entry.to_dict())
            elif date_entry is not None and entry.start.date == date_entry.name:
                new_date = False

            if new_date:
                date_entry = TreeEntry(name=entry.start.date, is_open=open_flag, subdata=[ ])

            forecast_details = format_text_as_wrapped(entry.content.description.long.get_value(), number_of_characters_per_line=110)
            subentries = [ ]
            for line in forecast_details.split("\n"):
                if len(subentries) == 0:
                    subentries.append(TreeEntry(name="Detailed", is_open=False, value=line))
                else:
                    subentries.append(TreeEntry(name="", is_open=False, value=line))
            entry_subdata = [
                TreeEntry(name=entry.content.DisplayKeys.description, is_open=open_flag, value=f"{entry.content.description.short.get_value()}", subdata= subentries),
                TreeEntry(name=entry.content.DisplayKeys.temperature, is_open=True, value=f"{entry.content.temperature.get_value()} {entry.content.temperature.get_unit()}"),
                TreeEntry(name=entry.content.DisplayKeys.rainChance, is_open=True, value=f"{entry.content.rainChance.get_value()} {entry.content.rainChance.get_unit()}"),
            ]

            tree_entry = TreeEntry(name=entry.properties.name, is_open=open_flag, subdata=entry_subdata)
            date_entry.subdata.append(tree_entry)
        return entries
    

class TreeEntry():
    class Keys():
        name: str = "name"
        open: str = "open"
        subdata: str = "subdata"
        value: str = "value"

    def __init__(self, name: str, is_open: bool = False, subdata: list[Self] = [ ], value:str = ""):
        self.name = name
        self.open = is_open
        self.subdata: list[TreeEntry] = subdata
        self.value = value

    def to_dict(self) -> dict[str, Any]:
        subdata_list = [ ]
        for sub_entry in self.subdata:
            subdata_list.append(sub_entry.to_dict())
        if self.value:
            return {
                TreeEntry.Keys.name : self.name,
                TreeEntry.Keys.open : bool(self.open),
                TreeEntry.Keys.value : self.value, 
                TreeEntry.Keys.subdata : subdata_list
            }
        else:
            return {
                TreeEntry.Keys.name : self.name,
                TreeEntry.Keys.open : bool(self.open),
                TreeEntry.Keys.subdata : subdata_list
            }