from cProfile import label
from itertools import zip_longest
import tkinter as tk
from tkinter import Widget, messagebox

from PIL import ImageTk, Image
from gui.empyrean.datetime import EmpyreanDateTime

from gui.empyrean.notebook import Notebook
from gui.empyrean.labelframe import LabelFrame

from gui.icons.icons import icons

from utils.download_manager import DownloadStatus, ForecastDownloader, ForecastType
from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement
from utils.json.forecast import Forecast
from utils.json.location import Location

class ForecastViewer_Notebook(Notebook):

    def __init__(self, container, location: Location) -> None:
        self.location = location
        self.download_manager = None

        super().__init__(container)

        self.sub_frame_names = [ ]
        self.sub_button_names = [ ]

        self.__create_frames()
        self.__add_icon()

        self.__bind_buttons()

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

    def __add_icon(self):

        ## TODO :: Get to properly display on the NE corner of the frame
        ## TODO :: Add functionality that, on click, copies the forecast to clipboard

        for frame_name in self.sub_frame_names:
            images = { }
            for icon_name, icon_path in icons.items():
                img = Image.open(icon_path)
                img = img.resize((24, 24), Image.ANTIALIAS)
                images[icon_name] = ImageTk.PhotoImage(img)
            
            buttonFrame = LabelFrame(self.subframes[frame_name][WidgetType.LABELFRAME])
            buttonFrame.columnconfigure(0, weight=1)
            buttonFrame.columnconfigure(1, weight=1)
            buttonFrame.rowconfigure(0, weight=1)

            column_counter = 0
            for name, img in images.items():
                buttonFrame.add_widget(
                    widget= tk.Button(buttonFrame, image=img),
                    widget_type= WidgetType.BUTTON,
                    widget_name= (frame_name + name.title()),
                    placement= GridPlacement(col=column_counter, row = 0, span={"col":1, "row":1}, sticky=tk.NE)
                )
                buttonFrame.widgets[WidgetType.BUTTON][(frame_name + name.title())].image = img
                column_counter += 1
                self.sub_button_names.append((frame_name + name.title()))

            self.subframes[frame_name][WidgetType.LABELFRAME].add_frame(
                frame= buttonFrame,
                type= WidgetType.LABELFRAME,
                name = f"{frame_name}_Buttons",
                placement = GridPlacement(col=3, row=0, sticky=tk.NE)
            )

    def __bind_buttons(self):

        # TODO:: Probably clean up the nested call from hell I've made to access things... Or maybe I need to not nest so many frames?
        for frame_name in self.sub_frame_names:
            for button_name, button in self.subframes[frame_name][WidgetType.LABELFRAME].subframes[f'{frame_name}_Buttons'][WidgetType.LABELFRAME].widgets[WidgetType.BUTTON].items():
                for ftype in [ForecastType.HOURLY.value.title(), ForecastType.EXTENDED.value.title()]:
                    if button_name == f'{self.location.alias}' + f'{ftype}' + f'Download':
                        button.configure(command= lambda: self._on_click_get_forecast())
                    elif button_name == f'{self.location.alias}' + f'{ftype}' + f'Popout':
                        button.configure(command= lambda: self._on_click_get_markdown())


    def on_tab_change(self, event):

        tab_event_name = f'{self.location.alias}' + event.widget.tab('current')['text']
        tab_hourly_name = f'{self.location.alias}' + f'{ForecastType.HOURLY.value.title()}'
        tab_extended_name = f'{self.location.alias}' + f'{ForecastType.EXTENDED.value.title()}'

        if self.current_tab is not None:
            self.previous_tab = self.current_tab
        if tab_event_name == tab_hourly_name:
            self.current_tab = tab_hourly_name
        elif tab_event_name == tab_extended_name:
            self.current_tab = tab_extended_name
        print(f'\t{self.previous_tab=}, {self.current_tab=}')

    def _on_click_get_forecast(self):

        forecast_type = ForecastType.POINTS
        for type in [ForecastType.HOURLY, ForecastType.EXTENDED]:
            if (f'{self.location.alias}{type.value.title()}') == self.current_tab:
                forecast_type = type
        print(f'Forecast Request: {forecast_type.value} @ {self.location.alias}')
        # TODO:: Check if the forecast has already been downloaded (e.g., earlier today)

        # TODO:: Check if the forecast is still valid

        if self.download_manager is None:
            self.download_manager = ForecastDownloader()
            self._monitor_download_manager()
            self.download_manager.start_download(location=self.location, forecast_request_type=forecast_type)
        else:
            messagebox.showerror("Download in progress", "Please wait for the current download to finish before requesting another.")

    def _monitor_download_manager(self):
        if self.download_manager.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")
            self.update_forecast(self.download_manager.forecast_to_save, self.download_manager.forecast_type)
            self.download_manager.destroy()
            self.download_manager = None
        else:
            self.after(1000, self._monitor_download_manager)

    def _monitor_download_manager(self):
        if self.download_manager.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")
            self.update_forecast(self.download_manager.forecast_to_save, self.download_manager.forecast_type)
            self.download_manager.destroy()
            self.download_manager = None
        else:
            self.after(1000, self._monitor_download_manager)

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

        for r in range(1, counter + 1):
                self.subframes[forecast_type.value.title()][WidgetType.LABELFRAME].rowconfigure(r, weight=1)

        self.set_content(
                content= forecast_as_str,
                placements= placements
            )
    
    def set_content(self, content: list[str ], placements: list[GridPlacement]) -> None:
        print(self.current_tab)
        frame_to_update = self.subframes[self.current_tab][WidgetType.LABELFRAME]

        print(f'Updating {super().current_tab} {self.current_tab}')
        
        if WidgetType.LABEL not in frame_to_update.keys():
            label_index = 0
            for line, place in zip(content, placements):
                variable_string = tk.StringVar()
                variable_string.set(line)
                frame_to_update.add_changing_Label(
                    widget= tk.Label(frame_to_update, text=line, borderwidth=1, relief="groove", anchor="e"),
                    widget_type= WidgetType.LABEL,
                    widget_name= f"{self.location.alias}: Content {label_index}-{self.current_tab}",
                    placement= place,
                    variable_string= variable_string
                )
        else:
            label_aliases = [f'{self.location.alias}: Content {i}-{self.current_tab}' for i in range(1,len(content)+1)]
            frame_to_update.update_labels(label_aliases= label_aliases, new_text= content)
        
    def _on_click_get_markdown(self):
        print(f'Current view: {self.location.alias}: {self.current_tab}')