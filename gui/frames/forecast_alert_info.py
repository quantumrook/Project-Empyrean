import tkinter as tk
import tkinter.ttk as ttk

from gui.empyrean.labelframe import LabelFrame

from utils.WidgetEnum import WidgetType
from utils.gridplacement import GridPlacement


class ForecastAlertInfo_LabelFrame(LabelFrame):

    _title = "Weather Alert Info for"

    def __init__(self, container) -> None:
        super().__init__(container)

        self.__add_content()
        self.update_title(f'{self._title} <Location>')

    def __add_content(self):
        dummy_text = "N/A"

        widget_name = "alert_issued_label"
        alert_issued_label = ttk.Label(self, text="Alert Issued:")
        self.add_widget(
                widget=alert_issued_label, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=0, row=0, sticky=tk.E)
            )

        widget_name = "alert_issued_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        alert_issued_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=alert_issued_text, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=1, row=0, sticky=tk.EW)
            )

        widget_name = "alert_valid_till_label"
        alert_valid_till_label = ttk.Label(self, text="Vaild Until:")
        self.add_widget(
                widget=alert_valid_till_label, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=0, row=1, sticky=tk.E)
            )

        widget_name = "alert_valid_till_text"
        self.display_label_vars[widget_name] = tk.StringVar()
        self.display_label_vars[widget_name].set(dummy_text)

        alert_valid_till_text = ttk.Label(self, textvariable=self.display_label_vars[widget_name])
        self.add_widget(
                widget=alert_valid_till_text, 
                widget_type=WidgetType.LABEL, 
                widget_name=widget_name, 
                placement = GridPlacement(col=1, row=1, sticky=tk.EW)
            )

    