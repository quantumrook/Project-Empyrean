from cProfile import label
from itertools import zip_longest
import tkinter as tk

from PIL import ImageTk, Image

from gui.empyrean.notebook import Notebook
from gui.empyrean.labelframe import LabelFrame

from gui.icons.icons import icons

from utils.download_manager import ForecastDownloader, ForecastType
from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement
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
        frame_names = ['hourly', 'extended']
        for frame_name in frame_names:
            self.add_frame(
                frame= LabelFrame(self),
                type= WidgetType.LABELFRAME,
                name= frame_name,
                placement= GridPlacement(sticky=tk.NSEW)
            )

            for r in range(0,3):
                self.subframes[frame_name][WidgetType.LABELFRAME].columnconfigure(r, weight=1)
            
            for r in range(0,24):
                self.subframes[frame_name][WidgetType.LABELFRAME].rowconfigure(r, weight=1)
    
    def __add_icon(self):

        ## TODO :: Get to properly display on the NE corner of the frame
        ## TODO :: Add functionality that, on click, copies the forecast to clipboard

        img = Image.open(icons["popout"])
        img = img.resize((24, 24), Image.ANTIALIAS)
        popout_image = ImageTk.PhotoImage(img)
        self.subframes['hourly'][WidgetType.LABELFRAME].add_widget(
            widget= tk.Button(self.subframes['hourly'][WidgetType.LABELFRAME], image=popout_image),
            widget_type= WidgetType.BUTTON,
            widget_name= "Popout",
            placement= GridPlacement(col=2, row=0, span={"col":1, "row": 1}, sticky=tk.NE )
        )
        self.subframes['hourly'][WidgetType.LABELFRAME].widgets[WidgetType.BUTTON]["Popout"].image = popout_image


        img = Image.open(icons["download"])
        img = img.resize((24, 24), Image.ANTIALIAS)
        download_img = ImageTk.PhotoImage(img)
        self.subframes['hourly'][WidgetType.LABELFRAME].add_widget(
            widget= tk.Button(self.subframes['hourly'][WidgetType.LABELFRAME], image=download_img, command=lambda: self.get_forecast()),
            widget_type= WidgetType.BUTTON,
            widget_name= "Download",
            placement= GridPlacement(col=1, row=0, span={"col":1, "row": 1}, sticky=tk.NE )
        )
        self.subframes['hourly'][WidgetType.LABELFRAME].widgets[WidgetType.BUTTON]["Download"].image = download_img

    def get_forecast(self):
        if self.download_manager is None:
            download_manager = ForecastDownloader()
            download_manager.start_download(location=self.location, forecast_request_type=ForecastType.HOURLY)
            #download_manager = None

    def set_content(self, frame_id: tuple[str, WidgetType], content: list[str ], placements: list[GridPlacement]) -> None:
        frame_to_update = self.subframes[frame_id[0]][frame_id[1]]
        
        if WidgetType.LABEL not in frame_to_update.keys():
            label_index = 0
            for line, place in zip(content, placements):
                variable_string = tk.StringVar()
                variable_string.set(line)
                frame_to_update.add_changing_Label(
                    widget= tk.Label(frame_to_update, text=line),
                    widget_type= WidgetType.LABEL,
                    widget_name= f"Content {label_index}",
                    placement= place,
                    variable_string= variable_string
                )
        else:
            label_aliases = [f'Content {i}' for i in range(len(content))]
            frame_to_update.update_labels(label_aliases= label_aliases, new_text= content)
