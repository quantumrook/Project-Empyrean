import tkinter as tk
from tkinter import ttk
from gui.empyrean.labelframe import LabelFrame
from gui.empyrean.notebook import Notebook

from gui.frames.forecast_alert_info import ForecastAlertInfo_LabelFrame
from gui.frames.forecast_request_info import ForecastRequestInfo_LabelFrame
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook
from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement

from utils.private import *
from utils.json.private_reader import *


class MainWindow(tk.Tk):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self) -> None:
        super().__init__()

        self.title('Project Empyrean')
        self.geometry("800x1200")

        self.set_default_style()
        self.load_private_data()
        self.create_notebook_for_locations()

    def set_default_style(self) -> None:
        self.style = ttk.Style(self)
        self.style.configure('.',                   font=('Tahmoa', 10))
        self.style.configure('TLabelframe.Label',   font=('Tahoma', 11))
        self.style.configure('TNotebook.Tab',       font=('Tahoma', 11))

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{project_directory_path}\\Project-Empyrean\\utils\\private.json')
    
    def create_notebook_for_locations(self) -> None:
        self.forecast_viewers = Notebook(self)
        
        for location in self.locations:
            print(location.alias)
            viewer_holder = LabelFrame(self)

            viewer_holder.add_frame(
                frame= ForecastRequestInfo_LabelFrame(viewer_holder, location),
                type= WidgetType.LABELFRAME,
                name= f'{location.alias}_RequestInfo',
                placement= GridPlacement(sticky=tk.NSEW)
            )

            viewer_holder.add_frame(
                frame= ForecastAlertInfo_LabelFrame(viewer_holder, location),
                type= WidgetType.LABELFRAME,
                name= f'{location.alias}_AlertInfo',
                placement= GridPlacement(col=1, sticky=tk.NSEW)
            )

            viewer_holder.add_frame(
                frame= ForecastViewer_Notebook(viewer_holder, location),
                type= WidgetType.NOTEBOOK,
                name= f'{location.name}_ForecastViewer',
                placement= GridPlacement(col=0, row=1, span={"col":2, "row": 1}, sticky=tk.NSEW)
            )
            viewer_holder.columnconfigure(0, weight=1)
            viewer_holder.columnconfigure(1, weight=1)
            self.forecast_viewers.add_frame(
                frame= viewer_holder,
                type= WidgetType.LABELFRAME,
                subframe_name= location.alias,
                frame_title= location.name,
                placement= GridPlacement(sticky=tk.NSEW)
            )
        self.forecast_viewers.grid(column=0, row=0, sticky=tk.NSEW)
        self.forecast_viewers.columnconfigure(0, weight=1)
        self.forecast_viewers.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

    def create_notebooks_manually(self) -> None:
        self.forecast_viewers = Notebook(self)
        viewer_holder = LabelFrame(self)

        viewer_holder.add_frame(
            frame= ForecastRequestInfo_LabelFrame(viewer_holder, self.locations[0]),
            type= WidgetType.LABELFRAME,
            name= f'{self.locations[0].alias}_RequestInfo',
            placement= GridPlacement(sticky=tk.NSEW)
        )

        viewer_holder.add_frame(
            frame= ForecastAlertInfo_LabelFrame(viewer_holder, self.locations[0]),
            type= WidgetType.LABELFRAME,
            name= f'{self.locations[0].alias}_AlertInfo',
            placement= GridPlacement(col=1, sticky=tk.NSEW)
        )

        viewer_holder.add_frame(
            frame= ForecastViewer_Notebook(viewer_holder, self.locations[0]),
            type= WidgetType.NOTEBOOK,
            name= f'{self.locations[0].name}_ForecastViewer',
            placement= GridPlacement(col=0, span={"col":2, "row": 1}, sticky=tk.NSEW)
        )

        self.forecast_viewers.add_frame(
            frame= viewer_holder,
            type= WidgetType.LABELFRAME,
            subframe_name= self.locations[0].alias,
            frame_title= self.locations[0].name,
            placement= GridPlacement(sticky=tk.NSEW)
        )

        viewer_holder = LabelFrame(self)

        viewer_holder.add_frame(
            frame= ForecastRequestInfo_LabelFrame(viewer_holder, self.locations[1]),
            type= WidgetType.LABELFRAME,
            name= f'{self.locations[1].alias}_RequestInfo',
            placement= GridPlacement(sticky=tk.NSEW)
        )

        viewer_holder.add_frame(
            frame= ForecastAlertInfo_LabelFrame(viewer_holder, self.locations[1]),
            type= WidgetType.LABELFRAME,
            name= f'{self.locations[1].alias}_AlertInfo',
            placement= GridPlacement(col=1, sticky=tk.NSEW)
        )

        viewer_holder.add_frame(
            frame= ForecastViewer_Notebook(viewer_holder, self.locations[1]),
            type= WidgetType.NOTEBOOK,
            name= f'{self.locations[1].name}_ForecastViewer',
            placement= GridPlacement(col=0, span={"col":2, "row": 1}, sticky=tk.NSEW)
        )

        self.forecast_viewers.add_frame(
            frame= viewer_holder,
            type= WidgetType.LABELFRAME,
            subframe_name= self.locations[0].alias,
            frame_title= self.locations[0].name,
            placement= GridPlacement(sticky=tk.NSEW)
        )
        self.forecast_viewers.grid(column=0, row=0, sticky=tk.NSEW)
        print('-----\nDone creating nested notebooks')