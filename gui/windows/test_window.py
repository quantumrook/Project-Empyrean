
import tkinter as tk

import TKinterModernThemes as TKMT
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from utils.private.private import *
from utils.reader import *
from utils.structures.forecast.forecast import Forecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import *


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.locations: list[Location] = [ ]
        self.forecasts: dict[str, dict[ForecastType, Forecast]] = { }
        self.load_private_data()

        self.control_frame = self.addFrame('controlButtons', row=0, col=0, padx=0, pady=0, sticky=tk.E)
        self.add_control_buttons()

        self.frame = self.addFrame('forecastStuff', row=1, col=0, padx=0, pady=10)
        self.add_forecast_notebook()

        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{project_directory_path}\\Project-Empyrean\\utils\\private.json')
        forecasts = None
        for location in self.locations:
            self.forecasts[location.alias] = { }
            for forecast_type in [ForecastType.HOURLY, ForecastType.EXTENDED]:
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

        forecast_types = [ForecastType.HOURLY, ForecastType.EXTENDED]
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
            for forecast_type in forecast_types:
                subframe = self.forecast_notebooks[f'{location.alias}'].addTab(f"{forecast_type.name.title()}")
                match forecast_type:
                    case ForecastType.HOURLY:
                        hourly_frame = Hourly_DisplayFrame(subframe, 'ForecastDisplayClass', None, location)
                    case ForecastType.EXTENDED:
                        continue
