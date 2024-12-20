import tkinter as tk
import tkinter.ttk as ttk

from gui.empyrean.labelframe import LabelFrame

from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement


class ForecastRequestInfo_LabelFrame(LabelFrame):

    _title = "Forecast Info for"

    def __init__(self, container) -> None:
        super().__init__(container)
        self.__add_content()
        self.update_title(f'{self._title} <Location>')

        if self.container.locations:
            self.update_title(f'{self._title} {self.container.locations[0]["name"]}')
        

    def __add_content(self):
        dummy_text = "YYYY-MM-DD HH:MM"

        widget_name = "last_request_label"
        last_request_label = ttk.Label(self, text="Last Forecast Request:")
        self.add_widget(
                widget=last_request_label, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=0, row=0, sticky=tk.E)
            )

        widget_name = "last_request_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        last_request_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=last_request_text, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=1, row=0, sticky=tk.EW)
            )

        widget_name = "valid_till_label"
        valid_till_label = ttk.Label(self, text="Vaild Until:")
        self.add_widget(
                widget=valid_till_label, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=0, row=1, sticky=tk.E)
            )

        widget_name = "valid_till_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        valid_till_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=valid_till_text, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=1, row=1, sticky=tk.EW)
            )

