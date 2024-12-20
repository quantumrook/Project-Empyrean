import tkinter as tk

from gui.empyrean.notebook import Notebook
from gui.empyrean.labelframe import LabelFrame

from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement

class ForecastViewer_Notebook(Notebook):
    
    def __init__(self, container) -> None:
        super().__init__(container)

        self.__create_frames()

    def __create_frames(self):
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
