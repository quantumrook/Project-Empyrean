
import tkinter as tk

import TKinterModernThemes as TKMT
from gui.frames.forecast.extended_display import Extended_DisplayFrame
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from utils.private.private import directory_paths
from utils.reader import *
from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import *


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.locations: list[Location] = [ ]
        self.forecasts: dict[str, dict[ForecastType, EmpyreanForecast]] = { }
        self.load_private_data()

        self.control_frame = self.addFrame('controlButtons', row=0, col=0, padx=0, pady=0, sticky=tk.E)
        self.add_control_buttons()

        self.frame = self.addFrame('forecastStuff', row=1, col=0, padx=0, pady=10)
        self.add_forecast_notebook()

        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')
        forecasts = None
        for location in self.locations:
            self.forecasts[location.alias] = { }
            for forecast_type in ForecastType.list():
                self.forecasts[location.alias][forecast_type] = None
    
    def add_control_buttons(self) -> None:
        self.control_frame.Button("Hi", None, row=0, col=0, padx=2, pady=0)
        self.control_frame.Button("Export", None, row=0, col=1, padx=2, pady=0)

    def add_forecast_notebook(self) -> None:
        self.forecast_notebook = self.frame.Notebook(
                name = "",
                row = 0,
                col = 0,
                sticky = "nsew",
                padx=0,
                pady=0
            )

        self.forecast_notebooks = { }

        today = EmpyreanDateTime()

        forecast_types = ForecastType.list()
        for location in self.locations:
            frame = self.forecast_notebook.addTab(f"{location.name}")
            self.forecast_notebooks[f'{location.alias}'] = frame.Notebook(
                name = f"sub{location.alias}",
                row=0,
                col=0,
                sticky = "nsew",
                padx=0,
                pady=0
            )

            hourly = self.try_get_data(location.name, ForecastType.HOURLY.value, today.date)
            extended = self.try_get_data(location.name, ForecastType.EXTENDED.value, today.date)
            for forecast_type in forecast_types:
                subframe = self.forecast_notebooks[f'{location.alias}'].addTab(f"{forecast_type.name.title()}")
                match forecast_type:
                    case ForecastType.HOURLY:
                        hourly_frame = Hourly_DisplayFrame(subframe, 'ForecastDisplayClass', hourly, extended, location)
                    case ForecastType.EXTENDED:
                        extended_frame = Extended_DisplayFrame(subframe, 'ForecastDisplayClass', hourly, extended, location)

    def try_get_data(self, location_name: str, forecast_type: str, date:str) -> None:
        file_path = f'{directory_paths["forecasts"]}\\{location_name}\\{forecast_type.title()}\\{date}.json'
        
        forecast_data_json = get_forecast_data(file_path)
        if forecast_data_json:
            return EmpyreanForecast.from_Empyrean(forecast_data_json)
        else:
            return None