"""Creates an extendable class for displaying forecast information.
"""
import tkinter as tk

import TKinterModernThemes as TKMT
from utils.reader import get_forecast_data
from utils.private.private import directory_paths
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable
from utils.text_wrapper import format_list_as_line_with_breaks


class ForecastDisplayFrame(TKMT.WidgetFrame):
    """Extends the TKMT WidgetFrame class to provide a base for the 
    hourly and extended forecast views.

    Args:
        TKMT (WidgetFrame): The TKMT class extended.
    """
    def __init__(self, master, name: str, location: Location):
        super().__init__(master, name)

        self.location = location

        self.hourly_forecast = WatchedVariable()
        self.hourly_forecast.on_change = self.on_hourly_forecast_change

        self.extended_forecast = WatchedVariable()
        self.extended_forecast.on_change = self.on_extended_forecast_change
        
        self.frame = self.addFrame(name="Forecast_Display_Container")
        self.info_frame = self.frame.addFrame(name="InfoFrame")
        self.setup_info_display()

    def setup_info_display(self) -> None:
        """Helper that adds widgets used by both subclasses.
        """
        self.info_frame.Label(
            text=format_list_as_line_with_breaks(
                list_to_compress= [
                        "Generated At:", 
                        "Last Updated:", 
                        "Valid Till:"
                    ],
                add_tab_spacing= False
            ),
            weight= "normal",
            size= 10,
            row= 1,
            col= 0,
            colspan = 1,
            rowspan = 1,
            sticky = tk.E
        )

    def on_hourly_forecast_change(self):
        """Callback contract that children should implement.
        """
        pass

    def on_extended_forecast_change(self):
        """Callback contract that children should implement.
        """
        pass

    def has_focus(self):
        """Callback contract that children should implement.
        """
        pass

    def try_get_data(self, forecast_type: ForecastType) -> EmpyreanForecast | None:
        """Helper function to load already downloaded forecast data.

        Args:
            forecast_type (ForecastType): The type of forecast to fetch

        Returns:
            EmpyreanForecast | None: The forecast for today's date of the specified type.
        """
        file_path = f'{directory_paths["forecasts"]}\\{self.location.name}\\{forecast_type.value.title()}\\{TODAY.date}.json'

        forecast_data_json = get_forecast_data(file_path)
        if forecast_data_json:
            return EmpyreanForecast.from_Empyrean(forecast_data_json)
        else:
            return None
