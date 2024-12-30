
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
from gui.notebooks.forecast_notebook import Forecast_Notebook
from gui.notebooks.location_notebook import Location_Notebook
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
        self.active_location = self.locations[0]
        self.forecast_notebook = Location_Notebook(self.frame, "locationViewer", self.locations)

    
    def add_new_location_tab(self):
        for location in self.locations:
            frame = self.forecast_notebook.addTab(location.name)
            forecastviews = Forecast_Notebook(frame, f"sub{location.alias}", location)

    def try_get_data(self, location_name: str, forecast_type: str, date:str) -> None:
        file_path = f'{directory_paths["forecasts"]}\\{location_name}\\{forecast_type.title()}\\{date}.json'

        forecast_data_json = get_forecast_data(file_path)
        if forecast_data_json:
            return EmpyreanForecast.from_Empyrean(forecast_data_json)
        else:
            return None

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