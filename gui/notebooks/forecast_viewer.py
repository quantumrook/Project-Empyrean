from cProfile import label
from itertools import zip_longest
import tkinter as tk
from tkinter import messagebox

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
    
    location = None

    def __init__(self, container, location: Location) -> None:
        super().__init__(container)

        self.location = location
        self.download_manager = None

        self.__create_frames()
        self.__add_icon()


    def __create_frames(self) -> None:
        frame_names = [ForecastType.HOURLY.value, ForecastType.EXTENDED.value]
        for frame_name in frame_names:
            self.add_frame(
                frame= LabelFrame(self),
                type= WidgetType.LABELFRAME,
                name= frame_name.title(),
                placement= GridPlacement(sticky=tk.NSEW)
            )

            self.subframes[frame_name.title()][WidgetType.LABELFRAME].columnconfigure(0, weight=1)
            self.subframes[frame_name.title()][WidgetType.LABELFRAME].columnconfigure(1, weight=2)
            self.subframes[frame_name.title()][WidgetType.LABELFRAME].columnconfigure(2, weight=1)
            self.subframes[frame_name.title()][WidgetType.LABELFRAME].columnconfigure(3, weight=1)

    def __add_icon(self):

        ## TODO :: Get to properly display on the NE corner of the frame
        ## TODO :: Add functionality that, on click, copies the forecast to clipboard

        for forecast_type in [ForecastType.HOURLY, ForecastType.EXTENDED]:
            images = { }
            for icon_name, icon_path in icons.items():
                img = Image.open(icon_path)
                img = img.resize((24, 24), Image.ANTIALIAS)
                images[icon_name] = ImageTk.PhotoImage(img)
            
            buttonFrame = LabelFrame(self.subframes[forecast_type.value.title()][WidgetType.LABELFRAME])
            buttonFrame.columnconfigure(0, weight=1)
            buttonFrame.columnconfigure(1, weight=1)
            buttonFrame.rowconfigure(0, weight=1)

            column_counter = 0
            for name, img in images.items():
                buttonFrame.add_widget(
                    widget= tk.Button(buttonFrame, image=img, command=lambda: self._on_click_get_forecast()),
                    widget_type= WidgetType.BUTTON,
                    widget_name= name.title(),
                    placement= GridPlacement(col=column_counter, row = 0, span={"col":1, "row":1}, sticky=tk.NE)
                )
                buttonFrame.widgets[WidgetType.BUTTON][name.title()].image = img
                column_counter += 1

            self.subframes[forecast_type.value.title()][WidgetType.LABELFRAME].add_frame(
                frame= buttonFrame,
                type= WidgetType.LABELFRAME,
                name = f"{forecast_type.value}_Buttons",
                placement = GridPlacement(col=3, row=0, sticky=tk.NE)
            )

    def _on_click_get_forecast(self):

        forecast_type = ForecastType.POINTS
        for type in [ForecastType.HOURLY, ForecastType.EXTENDED]:
            if type.value.title() == self.current_tab:
                forecast_type = type

        print(forecast_type)
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
        frame_to_update = self.subframes[self.current_tab][WidgetType.LABELFRAME]

        print(f'Updating {self.current_tab}')
        
        if WidgetType.LABEL not in frame_to_update.keys():
            label_index = 0
            for line, place in zip(content, placements):
                variable_string = tk.StringVar()
                variable_string.set(line)
                frame_to_update.add_changing_Label(
                    widget= tk.Label(frame_to_update, text=line, borderwidth=1, relief="groove", anchor="e"),
                    widget_type= WidgetType.LABEL,
                    widget_name= f"Content {label_index}-{self.current_tab}",
                    placement= place,
                    variable_string= variable_string
                )
        else:
            label_aliases = [f'Content {i}-{self.current_tab}' for i in range(len(content))]
            frame_to_update.update_labels(label_aliases= label_aliases, new_text= content)
        
