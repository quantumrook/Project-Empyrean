
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

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.root.geometry("1024x1024")

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

        self.at_a_glance_frame = At_A_Glance_Frame(self.root, "AtAGlanceFrame")

        self.frame = self.addFrame('forecastStuff', row=2, col=0, padx=0, pady=10, sticky=tk.NSEW)
        self.add_location_notebook()

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=6)

        self.request_window = None

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')

    def add_location_notebook(self) -> None:
        self.location_notebook = Location_Notebook(self.frame, "locationViewer", self.locations, self.at_a_glance_frame)

    def _on_click_get_markdown(self):
        print("Not implemented yet!")

    def _on_click_get_forecast(self):
        active_location = self.location_notebook.active_location.value
        if self.__points_is_valid() == False:

            self.request_window = RequestThreadManager_Window()
            print(f'Forecast Request: {RequestType.POINTS.value} @ {active_location.alias}')
            self.request_window.enqueue_download(active_location, RequestType.POINTS)

            #TODO :: Add in option to bypass points request anyways?

        for request_type in [RequestType.HOURLY, RequestType.EXTENDED]:
            hourly_tab = self.location_notebook.location_tabs[active_location.name].hourly_tab
            extended_tab = self.location_notebook.location_tabs[active_location.name].extended_tab
            if hourly_tab.hourly_forecast.value is not None and extended_tab.extended_forecast.value is not None:
                #TODO :: Display a message?
                messagebox.showinfo("Forecast Information", "You already have today's forecast.")
                continue
            # TODO:: Check if the forecast is still valid

            if self.request_window is None:
                self.request_window = RequestThreadManager_Window()

            print(f'Forecast Request: {request_type.value} @ {active_location.alias}')
            self.request_window.enqueue_download(location=active_location, forecast_request_type=request_type)

        if self.request_window is not None:
            self.request_window.monitor_queue()
            self._monitor_requests()

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")

            self.request_window.destroy()
            self.request_window = None
            self.location_notebook.trigger_refresh()
        else:
            self.root.after(1000, self._monitor_requests)

    def __points_is_valid(self) -> bool:
        active_location = self.location_notebook.active_location.value
        date = active_location.api_grid.lastverified
        last_verified = EmpyreanDateTime.from_Empyrean({
            EmpyreanDateTime.Keys.time_zone : active_location.timezone,
            EmpyreanDateTime.Keys.date : date,
            EmpyreanDateTime.Keys.time : "01:00"
            })
        return EmpyreanDateTime.is_in_range(
                questionable_datetime=TODAY,
                starting_datetime=last_verified,
                ending_datetime=EmpyreanDateTime.add_days(last_verified, 14)
            )