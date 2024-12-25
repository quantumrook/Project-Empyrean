import tkinter as tk
from tkinter import messagebox


from gui.empyrean.labelframe import LabelFrame
from gui.empyrean.notebook import Notebook
from gui.widget_enum import WidgetType
from gui.windows.request_manager import *
from utils.download.download_status import *
from utils.structures.datetime import EmpyreanDateTime
from utils.structures.forecast.forecast import Forecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.grid_placement import GridPlacement
from utils.structures.location.location import Location


class ForecastViewer_Notebook(Notebook):

    def __init__(self, container, location: Location, control_buttons: list[tk.Button]) -> None:
        self.location = location
        self.request_window = None

        super().__init__(container)
        self.container = container

        self.control_buttons = control_buttons

        self.sub_frame_names = [ ]
        self.sub_button_names = [ ]

        self.__create_frames()

    def __create_frames(self) -> None:     
        frame_names = [f'{self.location.alias}' + f'{ForecastType.HOURLY.value.title()}', f'{self.location.alias}' + f'{ForecastType.EXTENDED.value.title()}']
        tab_names = [ForecastType.HOURLY.value.title(), ForecastType.EXTENDED.value.title()]
        for frame_name, tab_name in zip(frame_names, tab_names):
            self.add_frame(
                frame= LabelFrame(self),
                type= WidgetType.LABELFRAME,
                subframe_name= frame_name,
                frame_title= tab_name,
                placement= GridPlacement(sticky=tk.NSEW)
            )

            self.subframes[frame_name][WidgetType.LABELFRAME].columnconfigure(0, weight=1)
            self.subframes[frame_name][WidgetType.LABELFRAME].columnconfigure(1, weight=2)
            self.subframes[frame_name][WidgetType.LABELFRAME].columnconfigure(2, weight=1)
            self.subframes[frame_name][WidgetType.LABELFRAME].columnconfigure(3, weight=1)

            self.sub_frame_names.append(frame_name)

    def bind_buttons(self):
        for button_widget_name, button_widget in self.control_buttons.items():
            for forecast_type in [ForecastType.HOURLY.value.title(), ForecastType.EXTENDED.value.title()]:
                if self.current_tab == (f'{self.location.alias}' + f'{forecast_type}'):
                    if button_widget_name == 'Popout':
                        button_widget.configure(command = lambda: self._on_click_get_markdown())
                    elif button_widget_name == 'Download':
                        button_widget.configure(command = lambda: self._on_click_get_forecast())

    def unbind_buttons(self):
        for _, button_widget in self.control_buttons.items():
            button_widget.configure(command = None)

    def on_tab_change(self, event):
        if self.control_buttons is not None:
            self.unbind_buttons()
        tab_event_name = f'{self.location.alias}' + event.widget.tab('current')['text']
        tab_hourly_name = f'{self.location.alias}' + f'{ForecastType.HOURLY.value.title()}'
        tab_extended_name = f'{self.location.alias}' + f'{ForecastType.EXTENDED.value.title()}'

        if self.current_tab is not None:
            self.previous_tab = self.current_tab
        if tab_event_name == tab_hourly_name:
            self.current_tab = tab_hourly_name
        elif tab_event_name == tab_extended_name:
            self.current_tab = tab_extended_name
        if self.control_buttons is not None:
            self.bind_buttons()

    def _on_click_get_forecast(self):

        request_type = RequestType.POINTS

        # TODO:: Check if Points Data needs to be refreshed

        for type in RequestType.list():
            if (f'{self.location.alias}{type.value.title()}') == self.current_tab:
                request_type = type
        print(f'Forecast Request: {request_type.value} @ {self.location.alias}')
        # TODO:: Check if the forecast has already been downloaded (e.g., earlier today)

        # TODO:: Check if the forecast is still valid

        if self.request_window is None:
            self.request_window = RequestThreadManager_Window()
            self._monitor_requests()
            self.request_window.start_download(location=self.location, forecast_request_type=request_type)
        else:
            messagebox.showerror("Download in progress", "Please wait for the current download to finish before requesting another.")

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")
            forecast_type = self.request_window.request_type
            for type in ForecastType.list():
                if (f'{self.location.alias}{type.value.title()}') == self.current_tab:
                    forecast_type = type
            self.update_forecast(self.request_window.forecast_to_save, forecast_type)
            self.request_window.destroy()
            self.request_window = None
        else:
            self.after(1000, self._monitor_requests)

    def update_forecast(self, forecast: Forecast, forecast_type: ForecastType):
        forecast_as_str = [ ]
        placements = [ ]
        counter = 1
        for dt, data in forecast.forecasts.items():
            if forecast_type == ForecastType.HOURLY and dt.date == EmpyreanDateTime().date:
                if counter == 1:
                    forecast_as_str.append(f'{data.startTime.as_string()}:\n')
                else:
                    forecast_as_str.append(f'{data.startTime.time}:\n')
                placements.append(GridPlacement(col=0, row=counter, sticky=tk.EW))
                
                if data.detailed[0]:
                    forecast_as_str.append(f'{data.short}\n{data.detailed}')
                else:
                    forecast_as_str.append(f'{data.short}\n')
                placements.append(GridPlacement(col=1, row=counter, sticky=tk.EW))

                forecast_as_str.append(f'Temp:\nRain Chance:')
                placements.append(GridPlacement(col=2, row=counter, sticky=tk.EW))

                forecast_as_str.append(f'{data.temperature.value} {data.temperature.unit}\n{data.probabilityOfPrecipitation} %')
                placements.append(GridPlacement(col=3, row=counter, sticky=tk.EW))

                counter += 1
            elif forecast_type == ForecastType.EXTENDED:
                forecast_as_str.append(f'{data.startTime.as_string()}:\n')
                placements.append(GridPlacement(col=0, row=counter, sticky=tk.EW))
                
                if data.detailed[0]:
                    forecast_as_str.append(f'{data.short}\n{" ".join(data.detailed)}')
                else:
                    forecast_as_str.append(f'{data.short}\n')
                placements.append(GridPlacement(col=1, row=counter, sticky=tk.EW))

                forecast_as_str.append(f'Temp:\nRain Chance:')
                placements.append(GridPlacement(col=2, row=counter, sticky=tk.EW))

                forecast_as_str.append(f'{data.temperature.value} {data.temperature.unit}\n{data.probabilityOfPrecipitation} %')
                placements.append(GridPlacement(col=3, row=counter, sticky=tk.EW))

                counter += 1

        for subframe_name in self.sub_frame_names:
            if subframe_name == f'{self.location.alias}{forecast_type.value.title()}':
                for r in range(1, counter + 1):
                        self.subframes[subframe_name][WidgetType.LABELFRAME].rowconfigure(r, weight=1)

        self.set_content(
                content= forecast_as_str,
                placements= placements
            )
    
    def set_content(self, content: list[str ], placements: list[GridPlacement]) -> None:
        print(f'Updating content on {self.current_tab}')
        for frame_name in list(self.subframes.keys()):
            print(frame_name, self.subframes[frame_name][WidgetType.LABELFRAME])
        
        frame_to_update = self.subframes[self.current_tab][WidgetType.LABELFRAME]
        
        if WidgetType.LABEL not in frame_to_update.keys():
            label_index = 0
            column_width = round(self.container.container.winfo_width() * 2 / 5)
            for line, place in zip(content, placements):
                variable_string = tk.StringVar()
                variable_string.set(line)
                anchor = "w"
                if label_index % 2 == 1:
                    anchor = "e"
                else:
                    anchor = "w"
                frame_to_update.add_changing_Label(
                    widget= tk.Label(frame_to_update, text=line, borderwidth=1, relief="groove", anchor=anchor, wraplength=column_width),
                    widget_type= WidgetType.LABEL,
                    widget_name= f"{self.location.alias}: Content {label_index}-{self.current_tab}",
                    placement= place,
                    variable_string= variable_string,
                    wrap_text= True
                )
        else:
            label_aliases = [f'{self.location.alias}: Content {i}-{self.current_tab}' for i in range(1,len(content)+1)]
            frame_to_update.update_labels(label_aliases= label_aliases, new_text= content)
        
    def _on_click_get_markdown(self):
        print(f'Current view: {self.location.alias}: {self.current_tab}')
        print("Not implemented yet!")
