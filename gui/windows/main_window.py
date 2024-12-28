
import tkinter as tk
from typing import Any
import TKinterModernThemes as TKMT

from gui.frames.control_button_frame import ControlButtons_Frame
from gui.frames.forecast.extended_display import Extended_DisplayFrame
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from gui.windows.request_manager import RequestThreadManager_Window

from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.private.private import directory_paths
from utils.reader import *
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import *


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = 0

    active_location: Location = None
    display_frames: dict[Location, dict[ForecastType, Any]] = None

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.root.geometry("1024x768")

        self.current_tab = None
        self.previous_tab = None

        self.locations: list[Location] = [ ]
        self.forecasts: dict[str, dict[ForecastType, EmpyreanForecast]] = { }
        self.load_private_data()

        self.controlbuttons_container = self.addFrame(name='cb_frame', row=0, col=0)
        self.controlbuttons_frame = ControlButtons_Frame(
            master= self.controlbuttons_container, 
            frame= self.addFrame('controlButtons', row=0, col=0, padx=0, pady=0, sticky=tk.E), 
            commands={
                    "popout" : lambda: self._on_click_get_markdown(),
                    "download" : lambda: self._on_click_get_forecast()
                }
            )


        self.frame = self.addFrame('forecastStuff', row=1, col=0, padx=0, pady=10, sticky=tk.NSEW)
        self.add_forecast_notebook()

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=9)

        self.request_window = None

        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')
        forecasts = None
        for location in self.locations:
            self.forecasts[location.alias] = { }
            for forecast_type in ForecastType.list():
                self.forecasts[location.alias][forecast_type] = None

    def add_forecast_notebook(self) -> None:
        self.forecast_notebook = self.frame.Notebook(
                name = f"",
                row = 0,
                col = 0,
                sticky = "nsew",
                padx=0,
                pady=0
            )
        self.forecast_notebook.notebook.name ="woof"
        self.forecast_notebooks = { }

        self.display_frames = { }

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

            self.forecast_notebooks[f'{location.alias}'].notebook.name = f"{location.alias}"
            
            self.display_frames[f'{location.alias}'] = { }

            hourly = None#self.try_get_data(location.name, ForecastType.HOURLY.value, TODAY.date)
            extended = None#self.try_get_data(location.name, ForecastType.EXTENDED.value, TODAY.date)
            for forecast_type in forecast_types:
                subframe: TKMT.WidgetFrame = self.forecast_notebooks[f'{location.alias}'].addTab(f"{forecast_type.name.title()}")
                subframe.name = f"sub{location.alias}"    
                match forecast_type:
                    case ForecastType.HOURLY:
                        self.display_frames[f'{location.alias}'][forecast_type] = Hourly_DisplayFrame(subframe, 'ForecastDisplayClass', hourly, extended, location)
                    case ForecastType.EXTENDED:
                        self.display_frames[f'{location.alias}'][forecast_type] =  Extended_DisplayFrame(subframe, 'ForecastDisplayClass', hourly, extended, location)
                self.forecast_notebooks[f'{location.alias}'].notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.forecast_notebook.notebook.bind('<<NotebookTabChanged>>', self.on_location_tab_change)
        self.active_location = self.locations[0]

    def try_get_data(self, location_name: str, forecast_type: str, date:str) -> None:
        file_path = f'{directory_paths["forecasts"]}\\{location_name}\\{forecast_type.title()}\\{date}.json'
        
        forecast_data_json = get_forecast_data(file_path)
        if forecast_data_json:
            return EmpyreanForecast.from_Empyrean(forecast_data_json)
        else:
            return None

    def on_location_tab_change(self, event):
        for location in self.locations:
            if event.widget.tab('current')['text'] == location.name:
                self.active_location = location
        print(f"{self.active_location.alias=}")
        # self.trigger_forecast_load()

    def on_tab_change(self, event):
        self.trigger_forecast_load()

    def trigger_forecast_load(self):
        new_download_button_state = 'normal'
        for forecast, display_frame in self.display_frames[f'{self.active_location.alias}'].items():
            if display_frame.hourly_forecast is None and display_frame.extended_forecast is None:
                hourly = self.try_get_data(self.active_location.name, ForecastType.HOURLY.value, TODAY.date)
                extended = self.try_get_data(self.active_location.name, ForecastType.EXTENDED.value, TODAY.date)
                display_frame.update(hourly, extended)
            if display_frame.hourly_forecast is not None and display_frame.extended_forecast is not None:
                new_download_button_state = 'disabled'
        self.controlbuttons_frame.toggle_download_button_state(new_download_button_state)

    def _on_click_get_markdown(self):
        print(f'Current view: {self.locations[self.current_location_index].alias}: {self.current_tab}')
        print("Not implemented yet!")

    def _on_click_get_forecast(self):

        request_type = RequestType.POINTS

        # TODO:: Check if Points Data needs to be refreshed

        for type in [RequestType.HOURLY, RequestType.EXTENDED]:
            
            # TODO:: Check if the forecast has already been downloaded (e.g., earlier TODAY)
            # TODO:: Check if the forecast is still valid

            if self.request_window is None:
                self.request_window = RequestThreadManager_Window()
                
                print(f'Forecast Request: {request_type.value} @ {self.active_location.alias}')
                self.request_window.enqueue_download(location=self.active_location, forecast_request_type=type)
            else:
                print(f'Forecast Request: {request_type.value} @ {self.active_location.alias}')
                self.request_window.enqueue_download(location=self.active_location, forecast_request_type=type)
            # messagebox.showerror("Download in progress", "Please wait for the current download to finish before requesting another.")

        self.request_window.monitor_queue()
        self._monitor_requests()

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")

            self.request_window.destroy()
            self.request_window = None
            self.trigger_forecast_load()
        else:
            self.root.after(1000, self._monitor_requests)