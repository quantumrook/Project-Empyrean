
import tkinter as tk
from tkinter import messagebox
from typing import Any
import TKinterModernThemes as TKMT

from PIL import Image, ImageTk

from gui.frames.at_a_glance_frame import At_A_Glance_Frame
from gui.icons.icons import clock_icons, colored_clock_icons

from gui.frames.control_button_frame import ControlButtons_Frame
from gui.frames.forecast.extended_display import Extended_DisplayFrame
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from gui.windows.request_manager import RequestThreadManager_Window

from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.private.private import directory_paths
from utils.reader import *
from utils.structures.datetime import TODAY, EmpyreanDateTime
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import *


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = 0

    previous_location: Location = None
    active_location: Location = None
    display_frames: dict[Location, dict[ForecastType, Any]] = None

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.root.geometry("1024x1024")

        self.current_tab = None
        self.previous_tab = None

        self.locations: list[Location] = [ ]
        self.load_private_data()

        self.controlbuttons_container = self.addFrame(name='cb_frame', row=0, col=0)
        self.controlbuttons_frame = ControlButtons_Frame(
            master= self.controlbuttons_container,
            frame= self.addFrame('controlButtons', row=0, col=0, padx=0, pady=0, sticky=tk.EW),
            commands={
                    "popout" : lambda: self._on_click_get_markdown(),
                    "download" : lambda: self._on_click_get_forecast()
                },
            root_window= self
            )

        self.frame = self.addFrame('forecastStuff', row=2, col=0, padx=0, pady=10, sticky=tk.NSEW)
        self.add_forecast_notebook()

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=6)

        self.request_window = None

        self.at_a_glance_frame = At_A_Glance_Frame(self.root, "AtAGlanceFrame")


    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')

    def add_forecast_notebook(self) -> None:
        self.forecast_notebook = self.frame.Notebook(
                name = f"forecastViewer",
                row = 0,
                col = 0,
                sticky = "nsew",
                padx=0,
                pady=0
            )
        self.forecast_notebook.notebook.name ="tkForecastViewer"
        self.forecast_notebooks = { }

        self.display_frames = { }

        self.add_new_location_tab()
        self.forecast_notebook.notebook.bind('<<NotebookTabChanged>>', self.on_location_tab_change)
        self.active_location = self.locations[0]

    def add_new_location_tab(self):
        for location in self.locations:
            if location.alias in self.forecast_notebooks.keys():
                continue

            frame = self.forecast_notebook.addTab(location.name)
            frame.name = location.name
            self.forecast_notebooks[location.alias] = frame.Notebook(
                name = f"sub{location.alias}",
                row=0,
                col=0,
                sticky = "nsew",
                padx=0,
                pady=0
            )

            self.display_frames[location.alias] = { }
            for forecast_type in ForecastType.list():
                subframe: TKMT.WidgetFrame = self.forecast_notebooks[location.alias].addTab(forecast_type.name.title())
                subframe.name = f"sub{location.alias}"
                match forecast_type:
                    case ForecastType.HOURLY:
                        self.display_frames[location.alias][forecast_type] = Hourly_DisplayFrame(subframe.master, 'ForecastDisplayClass', location)
                    case ForecastType.EXTENDED:
                        self.display_frames[location.alias][forecast_type] = Extended_DisplayFrame(subframe.master, 'ForecastDisplayClass', location)
                self.forecast_notebooks[location.alias].notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

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
                if self.previous_location is None:
                    self.previous_location = self.active_location
                elif self.active_location != location:
                    self.previous_location = self.active_location
                    self.active_location = location
                    self.trigger_forecast_load()

    def on_tab_change(self, event):
        self.trigger_forecast_load()

    def trigger_forecast_load(self):
        new_download_button_state = 'normal'
        for forecast, display_frame in self.display_frames[self.active_location.alias].items():
            if display_frame.hourly_forecast.value is None and display_frame.extended_forecast.value is None:
                hourly = self.try_get_data(self.active_location.name, ForecastType.HOURLY.value, TODAY.date)
                self.at_a_glance_frame.hourly_forecast.value = hourly
                display_frame.hourly_forecast.value = hourly
                extended = self.try_get_data(self.active_location.name, ForecastType.EXTENDED.value, TODAY.date)
                display_frame.extended_forecast.value = extended
            if display_frame.hourly_forecast.value is not None and display_frame.extended_forecast.value is not None:
                new_download_button_state = 'disabled'
        self.controlbuttons_frame.toggle_download_button_state(new_download_button_state)
        

    def _on_click_get_markdown(self):
        print(f'Current view: {self.locations[self.current_location_index].alias}: {self.current_tab}')
        print("Not implemented yet!")

    def _on_click_get_forecast(self):

        if self.__points_is_valid() == False:

            self.request_window = RequestThreadManager_Window()
            print(f'Forecast Request: {RequestType.POINTS.value} @ {self.active_location.alias}')
            self.request_window.enqueue_download(self.active_location, RequestType.POINTS)

            #TODO :: Add in option to bypass points request anyways?

        for request_type in [RequestType.HOURLY, RequestType.EXTENDED]:
            forecast_type = ForecastType.from_string(request_type)
            if self.display_frames[self.active_location.alias][forecast_type].hourly_forecast.value is not None and self.display_frames[self.active_location.alias][forecast_type].extended_forecast.value is not None:
                #TODO :: Display a message?
                messagebox.showinfo("Forecast Information", "You already have today's forecast.")
                continue
            # TODO:: Check if the forecast is still valid

            if self.request_window is None:
                self.request_window = RequestThreadManager_Window()

            print(f'Forecast Request: {request_type.value} @ {self.active_location.alias}')
            self.request_window.enqueue_download(location=self.active_location, forecast_request_type=request_type)

        if self.request_window is not None:
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

    def __points_is_valid(self) -> bool:
        date = self.active_location.api_grid.lastverified
        last_verified = EmpyreanDateTime.from_Empyrean({
            EmpyreanDateTime.Keys.time_zone : self.active_location.timezone,
            EmpyreanDateTime.Keys.date : date,
            EmpyreanDateTime.Keys.time : "01:00"
            })
        return EmpyreanDateTime.is_in_range(
                questionable_datetime=TODAY,
                starting_datetime=last_verified,
                ending_datetime=EmpyreanDateTime.add_days(last_verified, 14)
            )