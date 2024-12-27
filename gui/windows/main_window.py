
import tkinter as tk
from typing import Any
from PIL import Image, ImageTk
import TKinterModernThemes as TKMT

from gui.frames.forecast.extended_display import Extended_DisplayFrame
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from gui.icons.icons import icons
from gui.windows.request_manager import RequestThreadManager_Window

from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.private.private import directory_paths
from utils.reader import *
from utils.structures.datetime import EmpyreanDateTime
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

        self.control_frame = self.addFrame('controlButtons', row=0, col=0, padx=0, pady=0, sticky=tk.E)
        self.add_control_buttons()

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
    
    def add_control_buttons(self) -> None:

        images = { }
        for icon_name, icon_path in icons.items():
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        row_counter = 0
        self.control_buttons = { }
        for name, img in images.items():
            button = self.control_frame.Button("", None, row=0, col=row_counter, widgetkwargs={"image" : img, "name" : name})
            button.image = img
            row_counter += 1

            self.control_buttons[name] = button

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

            self.forecast_notebooks[f'{location.alias}'].notebook.name = f"{location.alias}"
            
            self.display_frames[f'{location.alias}'] = { }

            hourly = self.try_get_data(location.name, ForecastType.HOURLY.value, today.date)
            extended = self.try_get_data(location.name, ForecastType.EXTENDED.value, today.date)
            for forecast_type in forecast_types:
                subframe = self.forecast_notebooks[f'{location.alias}'].addTab(f"{forecast_type.name.title()}")
                subframe.name = f"sub{location.alias}"    
                match forecast_type:
                    case ForecastType.HOURLY:
                        self.display_frames[f'{location.alias}'][forecast_type] = Hourly_DisplayFrame(subframe, 'ForecastDisplayClass', hourly, extended, location, self.control_buttons)
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
        if self.control_buttons is not None:
            self.unbind_buttons()
        
        print(f"Was: {self.active_location.alias}")
        for location in self.locations:
            if event.widget.tab('current')['text'] == location.name:
                self.active_location = location

        print(f"Now: {self.active_location.alias}")

        if self.control_buttons is not None:
            self.bind_buttons()

    def on_tab_change(self, event):
        if self.control_buttons is not None:
            self.unbind_buttons()

        print(f"Was: {self.current_tab}")
        self.current_tab = self.active_location.alias + event.widget.tab('current')['text']
        print(f"Now: {self.current_tab}")
        
        if self.control_buttons is not None:
            self.bind_buttons()


    def bind_buttons(self):
        has_data = False
        for forecast, display_frame in self.display_frames[f'{self.active_location.alias}'].items():
            display_frame.hourly_forecast = self.try_get_data(self.active_location.name, ForecastType.HOURLY.value, EmpyreanDateTime.now().date)
            display_frame.extended_forecast = self.try_get_data(self.active_location.name, ForecastType.EXTENDED.value, EmpyreanDateTime.now().date)
            if display_frame.hourly_forecast is not None and display_frame.extended_forecast is not None:
                has_data = True

        download_state = 'normal'
        if has_data == True:
            download_state = 'disabled'

        for name, button_widget in self.control_buttons.items():
            for forecast_type in ForecastType.list():
                if self.current_tab == (f'{self.locations[self.current_location_index].alias}' + f'{forecast_type.value.title()}'):
                    if name == 'Popout'.lower():
                        button_widget.configure(command = lambda: self._on_click_get_markdown())
                    elif name == 'Download'.lower():
                        button_widget['state'] = download_state
                        button_widget.configure(command = lambda: self._on_click_get_forecast())

    def unbind_buttons(self):
        for _, button in self.control_buttons.items():
            button.configure(command = None)

    def _on_click_get_markdown(self):
        print(f'Current view: {self.locations[self.current_location_index].alias}: {self.current_tab}')
        print("Not implemented yet!")

    def _on_click_get_forecast(self):

        request_type = RequestType.POINTS

        # TODO:: Check if Points Data needs to be refreshed

        for type in [RequestType.HOURLY, RequestType.EXTENDED]:
            
            # TODO:: Check if the forecast has already been downloaded (e.g., earlier today)
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

            for forecast, display_frame in self.display_frames[f'{self.active_location.alias}'].items():
                display_frame.hourly_forecast = self.try_get_data(self.active_location.name, ForecastType.HOURLY.value, EmpyreanDateTime.now().date)
                display_frame.extended_forecast = self.try_get_data(self.active_location.name, ForecastType.EXTENDED.value, EmpyreanDateTime.now().date)
                display_frame.refresh()

            self.request_window.destroy()
            self.request_window = None
            self.unbind_buttons()
            self.bind_buttons()
        else:
            self.root.after(1000, self._monitor_requests)