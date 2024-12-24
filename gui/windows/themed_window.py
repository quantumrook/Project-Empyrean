import tkinter as tk

import TKinterModernThemes as TKMT
from gui.empyrean.labelframe import LabelFrame
from gui.empyrean.notebook import Notebook
from gui.frames.forecast_alert_info import ForecastAlertInfo_LabelFrame
from gui.frames.forecast_buttons import ForecastButtons_LabelFrame
from gui.frames.forecast_request_info import ForecastRequestInfo_LabelFrame
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook
from gui.widget_enum import WidgetType
from utils.private.private import directory_paths
from utils.reader import *
from utils.structures.grid_placement import GridPlacement


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        self.load_private_data()
        self.create_notebook_for_locations()

        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')
    
    def create_notebook_for_locations(self) -> None:
        self.forecast_viewers = Notebook(self.master)

        for location in self.locations:
            print(location.alias)
            viewer_holder = LabelFrame(self.master)

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
                frame= ForecastButtons_LabelFrame(viewer_holder, location),
                type= WidgetType.LABELFRAME,
                name= f'{location.alias}_Buttons',
                placement= GridPlacement(col=2, sticky=tk.NSEW)
            )

            control_buttons = viewer_holder.subframes[f'{location.alias}_Buttons'][WidgetType.LABELFRAME].get_buttons()

            viewer_holder.add_frame(
                frame= ForecastViewer_Notebook(viewer_holder, location, control_buttons),
                type= WidgetType.NOTEBOOK,
                name= f'{location.name}_ForecastViewer',
                placement= GridPlacement(col=0, row=1, span={"col":3, "row": 1}, sticky=tk.NSEW)
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
