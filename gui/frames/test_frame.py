import tkinter as tk
import tkinter.ttk as ttk

from gui.empyrean.labelframe import LabelFrame
from gui.icons.icons import icons
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook

from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement


class Test_Frame(LabelFrame):

    _title = ""

    def __init__(self, container) -> None:
        super().__init__(container)

        self.__add_content()

    def __add_content(self):
        popout_image = tk.PhotoImage(file= icons["popout"])
        # self.add_widget(
        #     widget= ForecastViewer_Notebook(self),
        #     widget_type= WidgetType.NOTEBOOK,
        #     widget_name = "Forecast Viewer",
        #     placement= GridPlacement(col=0, row=0, span={"col":1, "row": 1}, sticky=tk.NW)
        # )
        # self.add_widget(
        #     widget= tk.Label(self, image=popout_image),
        #     widget_type= WidgetType.LABEL,
        #     widget_name = "Popout",
        #     placement= GridPlacement(col=1, row=0, span={"col":1, "row": 1}, sticky=tk.NE)
        # )


    