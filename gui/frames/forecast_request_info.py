import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

from empyrean.labelframe import LabelFrame
from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement


class ForecastRequestInfo_LabelFrame(LabelFrame):

    def __init__(self, container) -> None:
        super().__init__(container)

        self.__add_content()

    def __add_content(self):
        dummy_text = "YYYY-MM-DD HH:MM"

        widget_name = "last_request_label"
        last_request_label = ttk.Label(self, text="Last Forecast Request:")
        self.add_widget(
                widget=last_request_label, 
                type=WidgetType.LABEL, 
                name=widget_name, 
                placement = GridPlacement(col=0, row=0, sticky=tk.E)
            )

        widget_name = "last_request_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        last_request_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=last_request_text, 
                type=WidgetType.LABEL, 
                name=widget_name, 
                placement = GridPlacement(col=1, row=0, sticky=tk.EW)
            )

        widget_name = "valid_till_label"
        valid_till_label = ttk.Label(self, text="Vaild Until:")
        self.add_widget(
                widget=valid_till_label, 
                type=WidgetType.LABEL, 
                name=widget_name, 
                placement = GridPlacement(col=0, row=1, sticky=tk.E)
            )

        widget_name = "valid_till_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        valid_till_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=valid_till_text, 
                type=WidgetType.LABEL, 
                name=widget_name, 
                placement = GridPlacement(col=1, row=1, sticky=tk.EW)
            )

    